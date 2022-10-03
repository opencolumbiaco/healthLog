from django.shortcuts import render, redirect
from django.contrib import messages
from healthApp.models import *


def addWeek(request):
    if 'user_id' not in request.session:
        message.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        weeks = Week.objects.all().values()
        context = {
            'user': user,
            'weeks': weeks,
        }
        return render(request, 'createWeek.html', context)

def addLog(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        weeks = Week.objects.all().values()
        context = {
            'user': user,
            'weeks': weeks,
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

def createWeek(request):
    Week.objects.create(
        title=request.POST['title'],
        writer=User.objects.get(id=request.session['user_id']),
    )
    messages.error(request, 'Week Created')
    return redirect('/log/')

def createLog(request):
    Log.objects.create(
        day = request.POST['day'],
        title=request.POST['title'],
        content=request.POST['content'],
        week_id = request.POST['week'],
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

def viewWeek(request, week_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        week = Week.objects.get(id=week_id)
        logs = Log.objects.all().values()
        moods = Mood.objects.all().values()
        symptoms = Symptom.objects.all().values()
        context = {
                'user': user,
                'week': week,
                'logs': logs,
                'moods': moods,
                'symptoms': symptoms,
            }
        return render(request, 'viewWeek.html', context)

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

def updateLog(request, log_id):
    toUpdate=Log.objects.get(id=log_id)
    toUpdate.title = request.POST['title']
    toUpdate.content = request.POST['content']
    toUpdate.save()
    messages.error(request, 'Log Updated')
    return redirect(f'/log/{toUpdate.id}/view/')

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