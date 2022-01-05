#from astral import LocationInfo
from suncalc import getTimes
#city=LocationInfo("Jerusalem","Israel","Asia/Jerusalem",31.657652,35.123509)
from datetime import datetime,timedelta,timezone
#from astral.sun import sun
import requests
import json
now=lambda: datetime.now()
#getTime=lambda d:getTimes(d,31.657652,35.123509) #Har Etzion
getTime=lambda d:getTimes(d,32.089870,34.880450) #Petach Tikva
def currentHour():
  #yesterday=sun(city.observer,date=datetime.now()-timedelta(days=1),tzinfo=city.timezone)
  yesterday=getTime(datetime.now()-timedelta(days=1))
  #today=sun(city.observer,date=datetime.now(),tzinfo=city.timezone)
  today=getTime(datetime.now())
  #tommorow=sun(city.observer,date=datetime.now()+timedelta(days=1),tzinfo=city.timezone)
  tommorow=getTime(datetime.now()+timedelta(days=1))
  if now()<today['sunrise']:
    tommorow=today
    today=yesterday
  dayLength=(today['sunsetStart']-today['sunrise']).seconds/60/12
  nightLength=(tommorow['sunrise']-today['sunsetStart']).seconds/60/12
  day=now()<today['sunsetStart']
  length=dayLength if day else nightLength
  start=today['sunrise'] if day else today['sunsetStart']
  timeSinceStart=((now()-start).seconds/60)/length
  hour=int(timeSinceStart)
  minute=int((timeSinceStart-hour)*24)
  return str(hour)+':'+str(minute)
def firstHourOfTommorow():
    tommorow=getTime(datetime.now()+timedelta(days=1))
    length = (tommorow['sunsetStart']-tommorow['sunrise']).seconds/60/12
    return (tommorow['sunrise']+timedelta(minutes=length)).strftime("%H:%M:%S")
def weeklyDisplay():
  if datetime.today().weekday() in [4,5]:
    j=json.loads(requests.get('https://www.hebcal.com/shabbat?cfg=json&geonameid=%20281184&m=50').text)
    return '\t'.join([i['title'] for i in j['items']])
  return ""
def getInterval():
  if datetime.today().weekday() in [4,5]:
    return 60000
  return 1000
def getLength():
  yesterday=sun(city.observer,date=datetime.now()-timedelta(days=1),tzinfo=city.timezone)
  today=sun(city.observer,date=datetime.now(),tzinfo=city.timezone)
  tommorow=sun(city.observer,date=datetime.now()+timedelta(days=1),tzinfo=city.timezone)
  if now()<today['sunrise']:
    tommorow=today
    today=yesterday
  dayLength=(today['sunset']-today['sunrise']).seconds/60/12
  nightLength=(tommorow['sunrise']-today['sunset']).seconds/60/12
  if now()<today['sunset']:
    return dayLength
  else:
    return nightLength
def convertToTimed(hour):
  time=[int(i) for i in hour.split(':')];time=time if len(time)>2 else [0]+time
  minutes=timedelta(hours=time[0],minutes=time[1],seconds=time[2]).total_seconds()/60
  timedHour=minutes/getLength()
  fraction=lambda d:d-int(d)
  times=[timedHour];times.append(fraction(times[-1])*24);times.append(fraction(times[-1])*24);times.append(fraction(times[-1])*24);
  formattedTimes=[int(i) for i in times]
  return ("" if formattedTimes[0]==0 else (f"{formattedTimes[0]} שעות"+"\n")) + f"{formattedTimes[1]} עונות"+"\n"+f"{formattedTimes[2]} עיתים"+"\n"+f"{formattedTimes[3]} רגעים"
