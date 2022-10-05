from django.shortcuts import render, redirect
from django.contrib import messages
from healthApp.models import *


def index(request):
    if 'user_id'  not in request.session:
        return render(request, 'welcome.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        weeks = Week.objects.all().order_by('-updatedAt')
        logs = Log.objects.all().order_by('-updatedAt')
        context = {
            'user': user,
            'weeks': weeks,
            'logs': logs,
        }
        return render(request, 'index.html', context)