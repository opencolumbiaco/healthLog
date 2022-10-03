from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public
    path('', views.index),
    # Auth
    path('logReg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.register),
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
    # Symptom
    path('symptom/', views.symptoms),
    path('symptom/create/', views.createSymptom),
    path('symptom/<int:symptom_id>/update/', views.updateSymptom),
    path('symptom/<int:symptom_id>/delete/', views.deleteSymptom),
    path('user/dashboard/', views.profileDash),
    # Admin
    path('theAdmin/', views.theAdmin),
    path('theAdmin/user/', views.adminUsers),
    path('theAdmin/user/<int:user_id>/delete/', views.deleteUser),
    path('logout/', views.logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)