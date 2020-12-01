from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http import JsonResponse, HttpRequest
from .serializer import QuerySerializer, GetSerializer
from .regions import REGION_LIST
from Avito.celery import app, CELERYBEAT_SCHEDULE
from .models import *
from .get_time import gettime
from .tasks import counter
from datetime import timedelta
from typing import Dict, Any
# Create your views here.


@api_view(['GET', ])
def get_regions(request: HttpRequest) -> Dict[str, str]:
	if request.method == "GET":
		return Response(REGION_LIST)

@api_view(['POST', ])
def get_id_search(request: HttpRequest) -> Dict[str, Any]:
	if request.method == "POST":
		serializer = QuerySerializer(data=request.data)
		if serializer.is_valid():
			try:
				user = Query.objects.get(region=request.data['region'], search_query__iexact=request.data['search_query'])
				return Response({"Поисковый запрос": "Поисковый запрос с таким регионом уже существует"})
			except Query.DoesNotExist:
				if request.data['region'] not in REGION_LIST:
					return Response({"Регион": "Такого региона не существует"})
				temp = Query(region=request.data['region'], search_query=request.data['search_query'])
				temp.save()
				return Response({'ID': temp.id})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def get_request(request: HttpRequest) -> Dict[str, Any]:
	if request.method == "POST":
		serializer = GetSerializer(data=request.data)
		datas = []
		if serializer.is_valid():
			try:
				user = Query.objects.get(id=request.data['id'])
				requests = user.qr.all()
				date_start = gettime(request.data['date_start'])
				date_end = gettime(request.data['date_end'])
				for i in requests:
					if i.time > date_start and date_end > i.time:
						datas.append({'Время запроса': i.time, 'Количество результатов': i.count})
			except Query.DoesNotExist:
				return Response({'ID': 'Запроса с таким ID не существует'})
			return Response({'ID': user.id, 'Регион': REGION_LIST[user.region], 'Поисковый запрос': user.search_query, 'Список запросов': datas})
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)