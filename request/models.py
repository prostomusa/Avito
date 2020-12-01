from django.db import models


class Query(models.Model):
	region = models.CharField(max_length=50)
	search_query = models.CharField(max_length=100)

class Time(models.Model):
	query = models.ForeignKey(Query, on_delete = models.CASCADE, related_name='qr')
	count = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-time']
# Create your models here.