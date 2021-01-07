from __future__ import unicode_literals
from django.shortcuts import render

import json

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Survivor, Item
from myapp.serializers import SurvivorSerializer
from myapp.serializers import Survivor_LocationSerializer, ItemSerializer
from rest_framework import generics
from .services.tradeitems import Trader
from myapp.serializers import SurvivorSerializer
from rest_framework import status







class SurvivorCreate(generics.ListCreateAPIView):
    
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer


class SurvivorDetail(generics.ListCreateAPIView):

    def get(self, request, pk, format=None):
        survivor = get_object_or_404(Survivor, pk=pk)
        serializer = SurvivorSerializer(survivor)
        return Response(serializer.data)

class TradeItems(APIView, Trader):

    def get(self, request, pk_sur_1, pk_sur_2, format=None):
        survivor_1 = get_object_or_404(Survivor, pk=pk_sur_1)
        survivor_2 = get_object_or_404(Survivor, pk=pk_sur_2)
        serializer_1 = SurvivorSerializer(survivor_1)
        serializer_2 = SurvivorSerializer(survivor_2)
        data = ((serializer_1.data), (serializer_2.data))
        return JsonResponse(data, safe=False)

    def patch(self, request, pk_sur_1, pk_sur_2, format=None):
        survivor_1 = get_object_or_404(Survivor, pk=pk_sur_1)
        survivor_2 = get_object_or_404(Survivor, pk=pk_sur_2)
        trader = Trader(request, survivor_1, survivor_2)
        trade = trader.perform()
        if trade:
            serializer_1 = SurvivorSerializer(survivor_1)
            serializer_2 = SurvivorSerializer(survivor_2)
            data = ((serializer_1.data), (serializer_2.data))
            return JsonResponse(data, safe=False)
       