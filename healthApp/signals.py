from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Log)
def createLog(sender, instance, created, **kwargs):
    if created:
        Upload.objects.create(log=instance)

@receiver(post_save, sender=Log)
def saveLog(sender, instance, **kwargs):
    instance.upload.save()