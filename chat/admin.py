from django.contrib import admin
from .models import ChatRoomMessage, User, FriendRequest, Profile, PublicChatRoomMessage


class ChatRoomMessageAdmin(admin.ModelAdmin):
    list_display = ("room_name" , 'user', "content", "date_sent")

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined')
    filter_horizontal = ("friend",)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('request_sender', 'request_receiver') 

class PublicChatRoomMessageAdmin(admin.ModelAdmin):
    list_display = ("user" , "content", "date_sent")

admin.site.register(User, UserAdmin)
admin.site.register(ChatRoomMessage, ChatRoomMessageAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Profile)
admin.site.register(PublicChatRoomMessage, PublicChatRoomMessageAdmin)