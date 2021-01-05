from __future__ import unicode_literals
from django.shortcuts import render

import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myapp.models import Survivor, Item
from myapp.serializers import SurvivorSerializer
from myapp.serializers import Survivor_LocationSerializer, ItemSerializer
from rest_framework import generics

class SurvivorCreate(generics.ListCreateAPIView):

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

class SurvivorDetail(generics.ListCreateAPIView):

    def get(self, request, pk, format=None):
        survivor = get_object_or_404(Survivor, pk=pk)
        serializer = SurvivorSerializer(survivor)
        return Response(serializer.data)