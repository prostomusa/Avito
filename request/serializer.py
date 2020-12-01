from rest_framework import serializers

from .models import *

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['region', 'search_query']


class GetSerializer(serializers.ModelSerializer):
	date_start = serializers.DateTimeField()
	date_end = serializers.DateTimeField()
	class Meta:
		model = Query
		fields = ['id', 'date_start', 'date_end']