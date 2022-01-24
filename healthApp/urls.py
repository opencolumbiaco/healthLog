from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('logReg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.register),
    path('logout/', views.logout),
    path('symptoms/', views.symptoms),
    path('addMood/', views.addMood),
    path('addLog/', views.addLog),
    path('createSymptom/', views.createSymptom),
    path('createLog/', views.createLog),
    path('createMood/', views.createMood),
    path('log/<int:log_id>/view/', views.viewLog),
    path('log/<int:log_id>/update/', views.updateLog),
    path('theAdmin/', views.theAdmin),
    path('theAdmin/allUsers/', views.adminUsers),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)