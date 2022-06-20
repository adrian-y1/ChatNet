from ast import Index
from time import strptime
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
import json
from django.contrib.auth.hashers import make_password, check_password

from django import forms
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sqlalchemy import all_
from .models import ChatRoomMessage, User, FriendRequest, Profile, PublicChatRoomMessage
from django.contrib import messages
from django.utils import timezone
import datetime
import pytz
import tzlocal
import time
from django.views.decorators.csrf import csrf_exempt


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']



def index(request):
    context = {
        'current_user_global': request.user
    }
    return render(request, "chat/index.html", context)


@login_required(login_url='/login')
def suggestions(request):
    all_users = User.objects.exclude(username=request.user)
    current_user = User.objects.get(username=request.user)
    context = {}
    
    if request.method == "POST":
        req_receiver = int(request.POST['req_receiver'])
        receiver_instance = User.objects.get(id=req_receiver)
        if 'req_sender' in request.POST:
            req_sender = int(request.POST['req_sender'])
            sender_instance = User.objects.get(id=req_sender)

        if request.POST.get('add') == 'Send Friend Request':
            create_req, created = FriendRequest.objects.get_or_create(request_sender=current_user, request_receiver=receiver_instance, sent=True, date_sent=timezone.localtime())
            create_req.save()
            return redirect('suggestions')
        # If user clciks on cancel button then delete the request from the database
        elif request.POST.get('cancel') == 'Cancel':
            cancel_req = FriendRequest.objects.get(request_sender=current_user, request_receiver=receiver_instance)
            cancel_req.delete()
            return redirect('suggestions')
        elif request.POST.get('accept') == 'Accept':
            sender_instance.friend.add(current_user)
            current_user.friend.add(sender_instance)
            try:
                f = FriendRequest.objects.get(request_sender=sender_instance, request_receiver=current_user)
                f.friends = True
                f.save()
            except FriendRequest.DoesNotExist:
                pass
            return redirect('suggestions')
        elif request.POST.get('decline') == 'Decline':
            try:
                delete_req = FriendRequest.objects.get(request_sender=sender_instance, request_receiver=current_user)
                delete_req.delete()
            except FriendRequest.DoesNotExist:
                pass
            return redirect('suggestions')
    try:
        data = []
        get_sender = FriendRequest.objects.filter(request_sender=current_user)
        for i in get_sender:
            data.append(i.request_receiver)
        context["get_sender"] = data
    except FriendRequest.DoesNotExist:
        pass


    try:
        receiver_data = []
        sender_data = []
        current_user_receiver = FriendRequest.objects.filter(request_receiver=current_user)
        for i in current_user_receiver:
            receiver_data.append(i)
            sender_data.append(i.request_sender)
        context['current_user_receiver'] = receiver_data
        context['sender_data'] = sender_data
        # Loop over senders and pass it to template
    except FriendRequest.DoesNotExist:
        pass
    store_non_friends = []

    for u in all_users:
        if u not in current_user.friend.all():
            store_non_friends.append(u)
            context["all_non_friends"] = store_non_friends
    print(store_non_friends)
    return render(request, 'chat/suggestions.html', context)

@login_required(login_url='/login')
def friends_list(request):
    instance = User.objects.get(username=request.user)
    friend_list = []
    context = {}

    if request.method == 'POST':
        friend_id = int(request.POST['friend_id'])
        friend_instance = User.objects.get(id=friend_id)
        if request.POST.get('remove') == 'Remove':
            instance.friend.remove(friend_instance)
            friend_instance.friend.remove(instance)

            try:
                retrieve_receiver_request = FriendRequest.objects.get(request_sender=friend_instance, request_receiver=instance, sent=True)
                retrieve_receiver_request.delete()
            except FriendRequest.DoesNotExist:
                try:
                    retrieve_sender_request = FriendRequest.objects.get(request_sender=instance, request_receiver=friend_instance, sent=True)
                    retrieve_sender_request.delete()
                except FriendRequest.DoesNotExist:
                    pass
            return redirect('friends_list')
            
    for friend in instance.friend.all():
        friend_list.append(friend)
        context["friendly_list"] = friend_list

    return render(request, 'chat/friends_list.html', context)


@login_required(login_url='/login')
def fetch_suggestions(request):
    all_users = User.objects.exclude(username=request.user)
    store_non_friends = []
    for u in all_users:
        if u not in request.user.friend.all():
            store_non_friends.append(u.serialize())
            
    return JsonResponse({'all_users': store_non_friends})


@login_required(login_url='/login')
def fetch_friends(request):
    instance = User.objects.get(username=request.user)
    all_friends = instance.friend.all()
    data = []
    for i in all_friends:
        data.append(i.serialize())
    return JsonResponse({"all_friends": data})


@login_required(login_url='/login')
def chat_room(request, username):
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "chat/error.html", {
            "err_msg": "The requested user does not exist."
        }) 
        
    all_users = User.objects.exclude(username=request.user)
    current_user = User.objects.get(username=request.user)

    # Change it to display an error
    if other_user not in current_user.friend.all():
        return render(request, "chat/error.html", {
            "err_msg": f"The requested user is not currently in your friends list. Add {other_user} to be able to message them."
        }) 
    

    # Create the room between the 2 users
    if  request.user.id > int(other_user.id):
        room_name = f"{request.user.id}-{other_user.id}"
    else:
        room_name = f"{other_user.id}-{request.user.id}"
    
    all_messages = ChatRoomMessage.objects.filter(room_name=room_name)

    return render(request, "chat/room.html", {
        "other_user": other_user,
        "all_users": all_users,
        "all_messages": all_messages,
        "current_time": datetime.datetime.now()
    })


def paginate_global_msg(request):
    all_messages = PublicChatRoomMessage.objects.all().order_by('-date_sent')

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    length_msg = len(all_messages)

    data = []
    try:
        for i in range(start, end + 1):
            data.append([all_messages[i].serialize(), {'user_img': all_messages[i].user.profile.picture.url}])
    except IndexError:
        end = len(all_messages) % 10
        for i in range(start, end):
            serialisation = [all_messages[i].serialize(), {'user_img': all_messages[i].user.profile.picture.url}]
            if serialisation not in data:
                data.append(all_messages[i].serialize())


    # Change the date from UTC to local timezone
    for d in data:
        date = d[0]['date_sent']
        date_obj = datetime.datetime.strptime(date, '%b %d %Y, %I:%M %S	%p')
        local_timezone = tzlocal.get_localzone()
        new_date = date_obj.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        # d["date_sent"] = new_date.strftime('%b %d %Y, %I:%M %p')
        difference = datetime.datetime.now() - new_date.replace(tzinfo=None)

        if difference.total_seconds() > 60:
            minutes = difference.total_seconds() / 60
            if minutes > 60:
                hours = difference.total_seconds() / 60**2
                if hours > 24:
                    if difference.days > 7:
                        weeks = difference.days / 7
                        if weeks > 4:
                            month = weeks / 4
                            if month > 12:
                                year = difference.days / 365
                                d[0]["date_sent"] = f"{int(year)}y ago"
                            else:
                                d[0]["date_sent"] = f"{int(month)}m ago"
                        else:
                            d[0]["date_sent"] = f"{int(weeks)}w ago"
                    else:
                        d[0]["date_sent"] = f"{int(difference.days)}d ago"
                else:
                    d[0]["date_sent"] = f"{int(hours)}h ago"
            else:
                d[0]["date_sent"] = f"{int(minutes)}m ago"
        else:
            d[0]["date_sent"] = f"{int(difference.total_seconds())}s ago"

    return JsonResponse({
        "messages_data": data,
        "length_msg": length_msg,
    })

    

@login_required(login_url="/login")
def paginate_msg(request, username):
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "chat/error.html", {
            "err_msg": "The Page requested does not exist. Please check the spelling of your request."
        }) 
    # Create the room between the 2 users
    if  request.user.id > int(other_user.id):
        room_name = f"{request.user.id}-{other_user.id}"
    else:
        room_name = f"{other_user.id}-{request.user.id}"

    all_messages = ChatRoomMessage.objects.filter(room_name=room_name).order_by('-date_sent')

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    length_msg = len(all_messages)

    data = []
    try:
        for i in range(start, end + 1):
            data.append(all_messages[i].serialize())
    except IndexError:
        end = len(all_messages) % 10
        for i in range(start, end):
            if all_messages[i].serialize() not in data:
                data.append(all_messages[i].serialize())

    # Change the date from UTC to local timezone
    for d in data:
        date = d['date_sent']
        date_obj = datetime.datetime.strptime(date, '%b %d %Y, %I:%M %S	%p')
        local_timezone = tzlocal.get_localzone()
        new_date = date_obj.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        # d["date_sent"] = new_date.strftime('%b %d %Y, %I:%M %p')
        difference = datetime.datetime.now() - new_date.replace(tzinfo=None)

        if difference.total_seconds() > 60:
            minutes = difference.total_seconds() / 60
            if minutes > 60:
                hours = difference.total_seconds() / 60**2
                if hours > 24:
                    if difference.days > 7:
                        weeks = difference.days / 7
                        if weeks > 4:
                            month = weeks / 4
                            if month > 12:
                                year = difference.days / 365
                                d["date_sent"] = f"{int(year)}y ago"
                            else:
                                d["date_sent"] = f"{int(month)}m ago"
                        else:
                            d["date_sent"] = f"{int(weeks)}w ago"
                    else:
                        d["date_sent"] = f"{int(difference.days)}d ago"
                else:
                    d["date_sent"] = f"{int(hours)}h ago"
            else:
                d["date_sent"] = f"{int(minutes)}m ago"
        else:
            d["date_sent"] = f"{int(difference.total_seconds())}s ago"

    return JsonResponse({
        "messages_data": data,
        "length_msg": length_msg
    })




@login_required(login_url="/login")
def profile(request, user_id):   

    try:
        user_profile = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, "chat/error.html", {
            "err_msg": "The requested user does not exist."
        }) 
    current_user = User.objects.get(username=request.user)

    local_timezone = tzlocal.get_localzone()
    new_date = user_profile.date_joined.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    user_profile.date_joined = new_date.strftime('%b %d %Y, %I:%M %p')

    context =  {
        "user_profile": user_profile,
        'date_joined': user_profile.date_joined,
        "profile_form": UserProfileForm()
    }

    if request.method == "POST":
        # This makes sure to get get the POST data for the current user instance's profile and since we are dealing with image files, get the file data as well
        if request.POST.get('update-pic') == 'Update':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect(f"/chat/profile/{user_id}")

        # If user clicks on send friend request button, get or create the object where current_user was the sender, and user_profile is the receiver then save it
        elif request.POST.get('add') == 'Send Friend Request':
            create_req, created = FriendRequest.objects.get_or_create(request_sender=current_user, request_receiver=user_profile, sent=True, date_sent=timezone.localtime())
            create_req.save()
            return redirect(f"/chat/profile/{user_id}")
        # If user clciks on cancel button then delete the request from the database
        elif request.POST.get('cancel') == 'Cancel':
            cancel_req = FriendRequest.objects.get(request_sender=current_user, request_receiver=user_profile, sent=True)
            cancel_req.delete()
            return redirect(f"/chat/profile/{user_id}")
        # if user clicks on accept, add them to each other's friend list
        elif request.POST.get('accept') == 'Accept':
            user_profile.friend.add(current_user)
            current_user.friend.add(user_profile)
            try:
                f = FriendRequest.objects.get(request_sender=user_profile, request_receiver=current_user)
                f.friends = True
                f.save()
            except FriendRequest.DoesNotExist:
                try:
                    get_f = FriendRequest.objects.get(request_sender=current_user, request_receiver=user_profile)
                    get_f.friends = True
                    get_f.save()
                except FriendRequest.DoesNotExist:
                    pass
            return redirect(f"/chat/profile/{user_id}")
        # if user clicks decline,try to see if the object exists, if it does, remove the friend request else pass
        elif request.POST.get('decline') == 'Decline':
            try:
                get_request = FriendRequest.objects.get(request_sender=user_profile, request_receiver=current_user)
                get_request.delete()
            except FriendRequest.DoesNotExist:
                pass
            return redirect(f"/chat/profile/{user_id}")
        # If user clicks on remove friend, remove the users from each others friend list
        elif request.POST.get('remove') == 'Remove Friend':
            user_profile.friend.remove(current_user)
            current_user.friend.remove(user_profile)

            # Try to see if the object exists where the request_sender was the user_profile and the receiver was the current user
            # if so, delete the request else try the reverse
            try:
                retrieve_receiver_request = FriendRequest.objects.get(request_sender=user_profile, request_receiver=current_user, sent=True)
                retrieve_receiver_request.delete()
            except FriendRequest.DoesNotExist:
                try:
                    retrieve_sender_request = FriendRequest.objects.get(request_sender=current_user, request_receiver=user_profile, sent=True)
                    retrieve_sender_request.delete()
                except FriendRequest.DoesNotExist:
                    pass
            return redirect(f"/chat/profile/{user_id}")
    try:
        get_sender = FriendRequest.objects.get(request_sender=current_user, request_receiver=user_profile)
        context["get_sender"] = get_sender
    except FriendRequest.DoesNotExist:
        pass

    try: 
        get_receiver = FriendRequest.objects.get(request_receiver=current_user, request_sender=user_profile)
        context["get_receiver"] = get_receiver
    except FriendRequest.DoesNotExist:
        pass

    return render(request, "chat/profile.html", context)


@login_required(login_url='/login')
def incoming_requests(request):
    current_user = User.objects.get(username=request.user)
    params = {
        'current_user': current_user
    }
    try:
        inc_req = FriendRequest.objects.filter(request_receiver=request.user).order_by('-date_sent')
        params["inc_req"] = inc_req
    except FriendRequest.DoesNotExist:
        pass

    if request.method == "POST":
        sender_id = int(request.POST['senderid'])
        sender = User.objects.get(id=sender_id)

        if request.POST.get('accept') == 'Accept':
            current_user.friend.add(sender)
            sender.friend.add(current_user)
            try:
                f = FriendRequest.objects.get(request_sender=sender_id, request_receiver=current_user)
                f.friends = True
                f.save()
            except FriendRequest.DoesNotExist:
                try:
                    get_f = FriendRequest.objects.get(request_sender=current_user, request_receiver=sender_id)
                    get_f.friends = True
                    get_f.save()
                except FriendRequest.DoesNotExist:
                    pass
            return redirect('incoming')
        elif request.POST.get('decline') == 'Decline':
            try:
                get_request = FriendRequest.objects.get(request_sender=sender, request_receiver=current_user)
                get_request.delete()
            except FriendRequest.DoesNotExist:
                pass
            return redirect('incoming')

    return render(request, 'chat/incoming.html', params)


@login_required(login_url='/login')
def outgoing_requests(request):
    current_user = User.objects.get(username=request.user)
    params = {
        'current_user': current_user
    }
    try:
        out_req = FriendRequest.objects.filter(request_sender=request.user).order_by('-date_sent')
        params["out_req"] = out_req
    except FriendRequest.DoesNotExist:
        pass

    if request.method == "POST":
        receiver_id = int(request.POST['receiverid'])
        receiver = User.objects.get(id=receiver_id)
        if request.POST.get('cancel') == "Cancel":
            cancel_req = FriendRequest.objects.get(request_sender=current_user, request_receiver=receiver, sent=True)
            cancel_req.delete()
        return redirect('outgoing')
    return render(request, 'chat/outgoing.html', params)

@login_required(login_url='/login')
def error_handling(request):
    return render(request, 'chat/error.html')

def change_password(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST['email']
        n_password = request.POST['npassword']
        cn_password = request.POST['cnpassword']

        if username == '':
            return render(request, "chat/change_password.html", {
                "message": "Username field cannot be blank."
            }) 
        if email == '':
            return render(request, "chat/change_password.html", {
                "message": "Email field cannot be blank."
            }) 
        if n_password == '':
            return render(request, "chat/change_password.html", {
                "message": "New Password field cannot be blank."
            }) 
        if cn_password == '':
            return render(request, "chat/change_password.html", {
                "message": "New Password Confirmation field cannot be blank."
            }) 
        
        user_auth = authenticate(request, username=username, email=email)
        
        if user_auth is not None:
            user = User.objects.get(username=username)
            user.password = make_password(n_password)
            user.save()
            return redirect('login')
        else:
            return render(request, "chat/change_password.html", {
                "message": "Invalid username and/or email and/or password."
            }) 


        
    return render(request, 'chat/change_password.html')


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
        
    return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })
        if len(username) < 3:
            return render(request, "chat/register.html", {
                "message": "Username must be atleast 3 characters long."
            })
        if username == '':
            return render(request, "chat/register.html", {
                "message": "Username field cannot be blank."
            })
        if email == '':
            return render(request, "chat/register.html", {
                "message": "Email field cannot be blank."
            })
        if password == '':
            return render(request, "chat/register.html", {
                "message": "Password field cannot be blank."
            })
        if confirmation == '':
            return render(request, "chat/register.html", {
                "message": "Password Confirmation field cannot be blank."
            })
        
        if len(password) < 6:
            return render(request, "chat/register.html", {
                "message": "Password must be atleast 6 characters long."
            })
        
        all_users = User.objects.all()
        for u in all_users:
            if username == u.username:
                return render(request, "chat/register.html", {
                    "message": "Username already taken."
                })
            elif email == u.email:
                return render(request, "chat/register.html", {
                    "message": "Email already taken."
                })
            
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, "chat/register.html")