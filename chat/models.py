from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    friend = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="friends")
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'friend': [user.username for user in self.friend.all()],
        }


class ChatRoomMessage(models.Model):
    room_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content} {self.room_name}"

    def serialize(self):
        return {
            'room_name': self.room_name,
            'user': self.user.serialize(),
            'content': self.content,
            'date_sent': self.date_sent.strftime("%b %d %Y, %I:%M %S %p")
        }

class PublicChatRoomMessage(models.Model):
    user = models.ForeignKey(User, related_name="user_public_messages", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} {self.user} {self.date_sent}"

    def serialize(self):
        return {
            'user': self.user.serialize(),
            'content': self.content,
            'date_sent': self.date_sent.strftime("%b %d %Y, %I:%M %S %p")
        }


class FriendRequest(models.Model):
    request_sender = models.ForeignKey(User, related_name='friend_requests_sender', on_delete=models.CASCADE)
    request_receiver = models.ForeignKey(User, related_name='friend_requests_receiver', on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    friends = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sender: {self.request_sender} Receiver: {self.request_receiver}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='default.png', upload_to='profile_pictures')

    def __str__(self):
        return f"{self.user}"
    
        
