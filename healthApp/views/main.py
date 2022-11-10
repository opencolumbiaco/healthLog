from django.shortcuts import render, redirect
from django.contrib import messages
from healthApp.models import *
# import tools for react data serialization
from rest_framework.views import APIView
from healthApp.models import *
from rest_framework.response import Response
from healthApp.serializer import *


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

def addNewMedication(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        meds = Medication.objects.all().values()
        context = {
            'user': user,
            'meds': meds,
        }
        return render(request, 'createNewMed.html', context)

def addMedication(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        meds = Medication.objects.all().values()
        logs = Log.objects.all().values()
        context = {
            'user': user,
            'meds': meds,
            'logs': logs,
        }
        return render(request, 'createMed.html', context)

def addSugar(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        logs = Log.objects.all().values()
        context = {
            'user': user,
            'logs': logs,
        }
        return render(request, 'createSugar.html', context)

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

def createMed(request):
    Medication.objects.create(
        name=request.POST['name'],
        dose=request.POST['dose'],
        freq=request.POST['freq'],
    )
    messages.error(request, 'Medication Added to list')
    return redirect('/add/medication/')

def createTaken(request):
    Taken.objects.create(
        when=request.POST['when'],
        medication_id=request.POST['medication'],
        day_id=request.POST['day'],
        member_id=request.POST['member'],
    )
    messages.error(request, 'Medication added to log')
    return redirect('/')

def createSugar(request):
    Sugar.objects.create(
        time=request.POST['time'],
        level=request.POST['level'],
        note_id=request.POST['note'],
        owner_id=request.POST['owner'],
    )
    messages.error(request, 'Entry saved to log')
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
        meds = Taken.objects.all().values()
        sugars = Sugar.objects.all().values()
        context = {
                'user': user,
                'week': week,
                'logs': logs,
                'moods': moods,
                'symptoms': symptoms,
                'meds': meds,
                'sugars': sugars,
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
        meds = Medication.objects.all().values()
        taken = Taken.objects.all().values()
        sugars = Sugar.objects.all().values()
        context = {
            'user': user,
            'log': log,
            'moods': moods,
            'symptoms': symptoms,
            'meds': meds,
            'taken': taken,
            'sugars': sugars,
        }
        # print('moods: ', moods)
        # print("symptoms: ", symptoms)
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


class ReactView(APIView):
    serializer_class = ReactSerializer
    # data gets passed into object for each item in the Food.Objects.all queryset
    # fields in data must match fields in model and serializer files
    def get(self, request):
        data = [
            {'foodsLogged': item.foodsLogged,
            'totalCalories': item.totalCalories,
            'date': item.date,
            'created': item.created,
            'updated': item.updated
            }
            for item in Food.objects.all()
        ]
        
        return Response(data)

    # post function adds form to REST framework on localhost 8000
    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)




