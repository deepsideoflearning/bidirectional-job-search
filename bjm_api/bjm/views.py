from django.shortcuts import render
from rest_framework import viewsets
from .models import BJM
from .serializers import BJMSerializer

class BJMView(viewsets.ModelViewSet):
    queryset = BJM.objects.all()
    serializer_class = BJMSerializer