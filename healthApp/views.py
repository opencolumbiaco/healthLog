from django.shortcuts import render, redirect
from django.contrib import messages
from healthApp.models import *
import bcrypt
from .special import ADMINKEY


def index(request):
    if 'user_id'  not in request.session:
        return render(request, 'welcome.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        logs = Log.objects.all().order_by('-updatedAt')
        context = {
            'user': user,
            'logs': logs,
        }
        return render(request, 'index.html', context)

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
    if request.POST['adminCode'] == ADMINKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=9
        toUpdate.save()
        return redirect('/')
    else:
        return redirect('/')

def symptoms(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        symptoms = Symptom.objects.all().values()
        context = {
            'user': user,
            'symptoms': symptoms,
        }
        return render(request, 'symptoms.html', context)

def addLog(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
        }
        return render(request, 'createLog.html', context)

def addMood(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        symptoms = Symptom.objects.all().values()
        logs = Log.objects.all().order_by('-updatedAt')
        context = {
            'user': user,
            'symptoms': symptoms,
            'logs': logs
        }
        return render(request, 'createMood.html', context)

def createSymptom(request):
    Symptom.objects.create(
        symptom=request.POST['symptom'],
        info=request.POST['info'],
    )
    messages.error(request, 'Symptom Created')
    return redirect('/symptom/')

def createLog(request):
    Log.objects.create(
        title=request.POST['title'],
        content=request.POST['content'],
        author=User.objects.get(id=request.session['user_id']),
    )
    messages.error(request, 'Log Created')
    return redirect('/')

def createMood(request):
    Mood.objects.create(
        tag=request.POST['tag'],
        date=request.POST['date'],
        mood=request.POST['mood'],
        symptom_id=request.POST['symptom'],
        log_id=request.POST['log'],
        user_id=request.POST['user_id']
    )
    messages.error(request, 'Symptom Entry Created')
    return redirect('/')

def viewLog(request, log_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        log = Log.objects.get(id=log_id)
        moods = Mood.objects.all().values()
        symptoms = Symptom.objects.all().values()
        context = {
            'user': user,
            'log': log,
            'moods': moods,
            'symptoms': symptoms,
        }
        print('moods: ', moods)
        print("symptoms: ", symptoms)
        return render(request, 'viewLog.html', context)

def editSymptom(request, symptom_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        symptom = Symptom.objects.get(id=symptom_id)
        content = {
            'user': user,
            'symptom': symptom,
        }
        return render(request, 'editSymptom.html', context)

def updateMood(request, mood_id):
    toUpdate=Mood.objects.get(id=mood_id)
    toUpdate.tag = request.POST['tag']
    toUpdate.date = request.POST['date']
    toUpdate.mood = request.POST['mood']
    toUpdate.symptom = request.POST['symptom']
    toUpdate.log_id = request.POST['log']
    toUpdate.user_id = request.POST['user_id']
    toUpdate.save()
    messages.error(request, 'Symptom Entry Updated')
    return redirect('/')

def updateSymptom(request, symptom_id):
    toUpdate=Symptom.objects.get(id=symptom_id)
    toUpdate.symptom = request.POST['symptom']
    toUpdate.info = request.POST['info']
    toUpdate.save()
    messages.error(request, 'Symptom Updated')
    return redirect('/symptom/')

def updateLog(request, log_id):
    toUpdate=Log.objects.get(id=log_id)
    toUpdate.title = request.POST['title']
    toUpdate.content = request.POST['content']
    toUpdate.save()
    messages.error(request, 'Log Updated')
    return redirect(f'/log/{toUpdate.id}/view/')

def deleteSymptom(request, symptom_id):
    toDelete=Symptom.objects.get(id=symptom_id)
    toDelete.delete()
    messages.error(request, 'Symptom Removed')
    return redirect('/symptom/')

def deleteLog(request, log_id):
    toDelete=Log.objects.get(id=log_id)
    toDelete.delete()
    messages.error(request, 'Log Removed')
    return redirect('/')

def deleteMood(request, mood_id):
    toDelete=Mood.objects.get(id=mood_id)
    toDelete.delete()
    messages.error(request, 'Symptom Entry Removed')
    return redirect('/')

def deleteUser(request, user_id):
    toDelete=User.objects.get(id=user_id)
    toDelete.delete()
    messages.error(request, 'User Removed')
    return redirect('/theAdmin/')

def theAdmin(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        if user.level == 9:
            logCount = Log.objects.all().count()
            moodCount = Mood.objects.all().count()
            symptomCount = Symptom.objects.all().count()
            userCount = User.objects.all().count()
            context = {
                'user': user,
                'logCount': logCount,
                'moodCount': moodCount,
                'symptomCount': symptomCount,
                'userCount': userCount,
            }
            print("log count: ", logCount, "mood count: ", moodCount, "symptom count: ", symptomCount)
            return render(request, 'admin/theAdmin.html', context)
        else:
            messages:error(request, "Please log in with an admin account")
            return redirect('/')

def adminUsers(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        users = User.objects.all().values()
        if user.level == 9:
            context = {
                'user': user,
                'users': users,
            }
            return render(request, 'admin/allUsers.html', context)
        else:
            messages:error(request, "Please log in with an admin account")
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