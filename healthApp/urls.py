from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public
    path('', views.index),
    path('exampleOne/dashboard/', views.exampleOne),
    path('exampleTwo/dashboard/', views.exampleTwo),
    path('exampleOne/mood/', views.exampleOneMood),
    path('exampleTwo/mood/', views.exampleTwoMood),
    # Auth
    path('logReg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.register),
    path('logout/', views.logout),
    path('user/dashboard/', views.profileDash),
    path('user/<int:user_id>/data/', views.profileData),
    path('user/<int:user_id>/edit/', views.editProfile),
    path('user/<int:user_id>/updateEmail/', views.updateEmail),
    path('user/<int:user_id>/updateUsername/', views.updateUsername),
    path('user/<int:user_id>/updateDiabetic/', views.updateDiabetic),
    path('user/<int:user_id>/updatePassword/', views.updatePassword),
    path('user/<int:user_id>/updateImage/', views.updateImage),
    path('user/addDoctor/', views.addDoctor),
    path('user/<int:user_id>/updateProvider/', views.updateToProvider),
    # Week
    path('week/', views.addWeek),
    path('week/create/', views.createWeek),
    path('week/<int:week_id>/view/', views.viewWeek),
    # Mood
    path('mood/', views.addMood),
    path('mood/create/', views.createMood),
    path('mood/<int:mood_id>/update/', views.updateMood),
    path('mood/<int:mood_id>/delete/', views.deleteMood),
    # Log
    path('log/', views.addLog),
    path('log/create/', views.createLog),
    path('log/<int:log_id>/view/', views.viewLog),
    path('log/<int:log_id>/update/', views.updateLog),
    path('log/<int:log_id>/delete/', views.deleteLog),
    # Messages
    path('user/messages/', views.viewAllMessages),
    path('user/portal/', views.messagePortal),
    path('user/messages/<int:message_id>/view/', views.viewMessage),
    path('user/messages/add/', views.addMessage),
    path('user/messages/create/', views.createMessage),
    path('user/messages/<int:message_id>/addReply/', views.createReply),
    path('user/messages/<int:message_id>/update/', views.updateMessage),
    path('user/messages/<int:reply_id>/updateReply/', views.updateReply),
    path('user/messages/<int:message_id>/delete/', views.deleteMessage),
    path('user/messages/<int:reply_id>/delete/', views.deleteReply),
    # Symptom
    path('symptom/', views.symptoms),
    path('symptom/create/', views.createSymptom),
    path('symptom/<int:symptom_id>/update/', views.updateSymptom),
    path('symptom/<int:symptom_id>/delete/', views.deleteSymptom),
    # Medication
    path('add/medication/', views.addNewMedication),
    path('medication/', views.addMedication),
    path('medication/create/', views.createMed),
    path('medication/log/create/', views.createTaken),
    path('medication/<int:medication_id>/edit/', views.editMedication),
    path('medication/<int:medication_id>/update/', views.updateMedication),
    # Sugar
    path('sugar/', views.addSugar),
    path('sugar/create/', views.createSugar),
    # Provider
    path('provider/dashboard/', views.providerDash),
    path('provider/notes/', views.providerNotes),
    path('provider/notes/<int:note_id>/view/', views.viewNote),
    path('provider/patient/<int:user_id>/view/', views.viewPatient),
    path('provider/patient/<int:user_id>/addNote/', views.addNote),
    path('provider/patient/<int:user_id>/createNote/', views.createNote),
    path('provider/notes/<int:note_id>/update/', views.updateNote),
    path('provider/notes/<int:note_id>/delete/', views.deleteNote),
    # Admin
    path('theAdmin/', views.theAdmin),
    path('theAdmin/user/', views.adminUsers),
    path('theAdmin/user/<int:user_id>/delete/', views.deleteUser),
    path('theAdmin/user/<int:user_id/makeAdmin/', views.makeAdmin),
    path('theAdmin/user/<int:user_id>/makeSuperAdmin/', views.makeSuperAdmin),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)