# post_save is a signal that is fired when a object is saved
from django.db.models.signals import post_save
# Sender
from .models import User, Profile
# receiver
from django.dispatch import receiver

# @receiver takes 2 args, a receiver and sender.
# create_profile function is creating a new profile object everytime a user is created for that user.
# When a user is saved then send the *Sender* signal which is then received by @receiver decorater which is the create_profile function-
# that takes the 4 args that the post_save signal is passing to it
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()

