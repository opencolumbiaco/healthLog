from django.db import models
from django.db.models.fields import BooleanField, CharField
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}

        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] = 'Username already in use'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=0)

    objects = UserManager()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profileImgs', default='bee.jpg')
    def __str__(self):
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class Symptom(models.Model):
    symptom = models.CharField(max_length=255)
    info = models.TextField(blank=True)
    def __str__(self):
        return self.symptom

class Log(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='theAuthor', on_delete=CASCADE)

    def __str__(self):
        return self.title

class Mood(models.Model):
    tag = models.CharField(max_length=255)
    date = models.DateTimeField()
    mood = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    symptom = models.ForeignKey(Symptom, related_name='theSymptom', on_delete=CASCADE)
    log = models.ForeignKey(Log, related_name='theLog',on_delete=CASCADE, blank=True)
    user = models.ForeignKey(User, related_name='UserMood', on_delete=CASCADE)


