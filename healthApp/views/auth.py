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

def profileDash(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else: 
        user = User.objects.get(id=request.session['user_id'])
        oneUser = user.id
        moods = Mood.objects.filter(user_id=oneUser).all().values()
        symptoms = Symptom.objects.all().values()
        GeneralHeadache = 0
        Migraine = 0
        Fatigue = 0
        PanicAttack = 0
        GeneralBackPain = 0
        ChronicBackPain = 0
        Depression = 0
        Anxiety = 0
        Fibromyalgia = 0
        AchesNPains = 0
        Other = 0
        userMoods = []
        for mood in moods:
            for symptom in symptoms:
                if mood['symptom_id'] == symptom['id']:
                    userMoods.append(symptom['symptom'])
        for ele in userMoods:
            if (ele =='General Headache'):
                GeneralHeadache = GeneralHeadache + 1
            elif (ele == 'Fatigue'):
                Fatigue = Fatigue + 1
            elif (ele == 'Panic Attack'):
                PanicAttack = PanicAttack + 1
            elif (ele == 'General Back Pain'):
                GeneralBackPain = GeneralBackPain + 1
            elif (ele == 'Migraine'):
                Migraine = Migraine + 1
            elif (ele == 'Chronic Back Pain'):
                ChronicBackPain = ChronicBackPain + 1
            elif (ele == 'Depression'):
                Depression = Depression + 1
            elif (ele == 'Anxiety'):
                Anxiety = Anxiety + 1
            elif (ele == 'Fibromyalgia'):
                Fibromyalgia = Fibromyalgia + 1
            elif (ele == 'Aches and Pains'):
                AchesNPains = AchesNPains + 1
            else:
                Other = Other + 1
        context = {
            'user': user,
            'moods': moods,
            'generalHeadache': GeneralHeadache,
            'migraine': Migraine,
            'fatigue': Fatigue,
            'panicAttack': PanicAttack,
            'generalBack': GeneralBackPain,
            'chronicBack': ChronicBackPain,
            'depression': Depression,
            'anxiety': Anxiety,
            'fibro': Fibromyalgia,
            'aches': AchesNPains,
            'other': Other,
        }
        return render(request, 'profile/profileData.html', context)

def editProfile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
        }
        return render(request, 'profile/editProfile.html', context)

def updateName(request, user_id):
    toUpdate=User.objects.get(id=user_id)
    toUpdate.firstName=request.POST['firstName']
    toUpdate.lastName=request.POST['lastName']
    toUpdate.save()
    messages.error(request, "Name has been updated")
    return redirect('/user/dashboard/')

def updateUsername(request, user_id):
    toUpdate=User.objects.get(id=user_id)
    errors = User.objects.updateUsername(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect(f'/user/{user_id}/edit/')
    toUpdate.username=request.POST['username']
    toUpdate.save()
    messages.error(request, "Username updated")
    return redirect('/user/dashboard/')

def updateEmail(request, user_id):
    toUpdate=User.objects.get(id=user_id)
    errors = User.objects.updateEmail(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect(f'/user/{user_id}/edit/')
    toUpdate.email=request.POST['email']
    toUpdate.save()
    messages.error(request, 'Email updated')
    return redirect('/user/dashboard/')

def updatePassword(request):
    pass

def updateImage(request):
    pass

def updateDiabetic(request, user_id):
    toUpdate=User.objects.get(id=user_id)
    toUpdate.profile.diabetic=request.POST['diabetic']
    toUpdate.save()
    messages.error(request, 'Updated Diabetic Question')
    return redirect('/user/dashboard/')