from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Symptom)
admin.site.register(Medication)
admin.site.register(Upload)
admin.site.register(Week)
admin.site.register(Log)
admin.site.register(Mood)
admin.site.register(Taken)
admin.site.register(Sugar)