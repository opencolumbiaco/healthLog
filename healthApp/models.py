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
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors

    def updateUsername(self, form):
        errors = {}
        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] = 'Username already in use'
        return errors
    
    def updateEmail(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
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
    def fullName(self):
        return f'{self.firstName} {self.lastName}'

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profileImgs', default='bee.jpg')
    diabetic = models.BooleanField(default=0)
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

class Medication(models.Model):
    name = models.CharField(max_length=255)
    dose = models.CharField(max_length=255)
    freq = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Upload(models.Model):
    medication = models.OneToOneField(Medication, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='medicationImgs', default='med.jpg')
    def __str__(self):
        return f'{self.medication.name} Upload'

def create_medication_upload(sender, instance, created, **kwargs):
    if created:
        Medication.objects.create(medication=instance)
        post_save.connect(create_medication_upload, sender=Medication)

class Week(models.Model):
    title = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(User, related_name='theWriter', on_delete=CASCADE)
    def __str__(self):
        return self.title

class Log(models.Model):
    day = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    week = models.ForeignKey(Week, related_name='theWeek', on_delete=CASCADE)
    author = models.ForeignKey(User, related_name='theAuthor', on_delete=CASCADE)

    def __str__(self):
        return f'{self.day} - {self.title}'

class Mood(models.Model):
    tag = models.CharField(max_length=255)
    date = models.DateTimeField()
    mood = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    symptom = models.ForeignKey(Symptom, related_name='theSymptom', on_delete=CASCADE)
    log = models.ForeignKey(Log, related_name='theLog',on_delete=CASCADE, blank=True)
    user = models.ForeignKey(User, related_name='UserMood', on_delete=CASCADE)

class Taken(models.Model):
    when = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    medication = models.ForeignKey(Medication, related_name='theMed', on_delete=CASCADE)
    day = models.ForeignKey(Log, related_name='theDay',on_delete=CASCADE, blank=True)
    member = models.ForeignKey(User, related_name='UserTaken', on_delete=CASCADE)

class Sugar(models.Model):
    time = models.DateTimeField()
    level = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    note = models.ForeignKey(Log, related_name='theNote',on_delete=CASCADE, blank=True)
    owner = models.ForeignKey(User, related_name='theOwner', on_delete=CASCADE)

# Food log table
class Food(models.Model):
    foodsLogged = models.TextField(null=True)
    totalCalories = models.IntegerField()
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

