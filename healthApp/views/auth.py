from django.shortcuts import render, redirect
from django.contrib import messages
from healthApp.models import *
import bcrypt

def logReg(request):
    if 'user_id'  not in request.session:
        return render(request, 'logReg.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        logs = Log.objects.all().order_by('-updatedAt')
        context = {
            'user': user,
            'logs': logs,
        }
        return render(request, 'index.html', context)

def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out')
    return redirect('/logReg/')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/logReg/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/logReg/')

def register(request):
    if request.method == 'GET':
        return redirect('/logReg/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/logReg/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        username = request.POST['username'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    if newUser.id == 1:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=9
        toUpdate.save()
        messages.error(request, "Welcome Admin Member")
        return redirect('/')
    if newUser.firstName == "Example":
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=5
        toUpdate.save()
        messages.error(request, "Welcome Example Account Member")
        return redirect('/')
    else:
        messages.error(request, "Welcome New Member")
        return redirect('/')
