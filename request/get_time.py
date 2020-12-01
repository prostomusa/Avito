from datetime import datetime, timezone
from Avito import settings
from django.utils.timezone import pytz
def gettime(time: str) -> datetime:
	year = int(time[0:4])
	month = int(time[5:7])
	day = int(time[8:10])
	hour = int(time[11:13])
	minute = int(time[14:16])
	second = int(time[17:19])
	return datetime(year, month, day, hour, minute, second)