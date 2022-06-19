from attr import Attribute
from .models import User, FriendRequest, ChatRoomMessage

from bs4 import BeautifulSoup

def get_friend_list(request):
    if request.user.is_authenticated:

        all_users = User.objects.get(username=request.user)
        friends_list = all_users.friend.all()
        

        return {"friends_list": friends_list}
    return {}

def get_all_users(request):
    if request.user.is_authenticated:
        all_users = User.objects.exclude(username=request.user)

        return {"all_users": all_users}
    return {}

def get_outgoing_requests(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        params = {}
        try:
            get_outgoing = FriendRequest.objects.filter(request_sender=request.user).exclude(friends=True)
            params["total"] = len(get_outgoing)
        except FriendRequest.DoesNotExist:
            pass
        return {"outgoing_num":params}
    return {}

def get_incoming_requests(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        params = {}
        try:
            get_incoming = FriendRequest.objects.filter(request_receiver=request.user).exclude(friends=True)
            
            params["total"] = len(get_incoming)
        except FriendRequest.DoesNotExist:
            pass
        return {"incoming_num":params}
    return {}

def get_last_message(request):
    if request.user.is_authenticated:

        all_users = User.objects.get(username=request.user)
        friends_list = all_users.friend.all()

        rooms = []
        data = []
        friend_data = []

        # turn current user's friends ids to strings in order to make comparisons with the room names and create them
        # then append the rooms to the list
        for friend in friends_list:
            if str(friend.id) not in friend_data:
                friend_data.append(str(friend.id))
            if friend.id > request.user.id:
                room_name = f"{friend.id}-{request.user.id}"
            else:
                room_name = f"{request.user.id}-{friend.id}"
            rooms.append(room_name)

        # Loop through all the rooms and get the last objects with the same room name from the database
        for i in rooms:
            all_rooms = ChatRoomMessage.objects.filter(room_name=i).last()
            if all_rooms is not None:
                data.append(all_rooms)
        
        # Using BeautifulSoup library, cut all HTML tags from the messages to display them tag free on the friends sidebar
        try:
            for d in data:
                text = d.content
                soup = BeautifulSoup(text, 'html.parser')
                if d.content is not None:
                    if '<h1>' in d.content:
                        d.content = soup.h1.text
                    if '<h2>' in d.content:
                        d.content = soup.h2.text
                    if '<h3>' in d.content:
                        d.content = soup.h3.text
                    if '<h4>' in d.content:
                        d.content = soup.h4.text
                    if '<p>' in d.content:
                        d.content = soup.p.text  
        except AttributeError:
            pass
        
        return {'last_message': data, 'check_friend': friend_data}
    return {}