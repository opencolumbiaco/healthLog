from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Symptom)
admin.site.register(Log)
admin.site.register(Upload)
admin.site.register(Mood)