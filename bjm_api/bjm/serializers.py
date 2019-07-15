from rest_framework import serializers
from .models import BJM

class BJMSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BJM
        fields = ('id', 'url', 'name', 'paradigm')
