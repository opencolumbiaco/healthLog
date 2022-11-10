from rest_framework import serializers
from healthApp.models import *

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['foodsLogged', 'totalCalories', 'date', 'created', 'updated']