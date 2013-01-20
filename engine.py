import datetime
from gitutils import datecommit

drawing = [
  [1,0,0,0,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1]
 ,[1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1]
]

def weekday(d):
  return int(d.strftime('%w'))

t = datetime.date.today()
today = datetime.datetime.fromordinal(t.toordinal()) + datetime.timedelta(hours = 12)
oneYearAgo = datetime.datetime(today.year-1, today.month, today.day, today.hour) 

firstWeekday = weekday(oneYearAgo) # 0 - Sunday, 6- Saturday
todayWeekday = weekday(today)

firstSunday = oneYearAgo + datetime.timedelta(days = 7 - firstWeekday)
lastSaturday = today - datetime.timedelta(days = (todayWeekday+1)%7)

for i in range(0,len(drawing[0])*7):
  date = firstSunday + datetime.timedelta(days = i)
  if drawing[weekday(date)][i/7] == 1:
    print str(date) + ' HIT GITHUB'
    for j in range(0,60):
      datecommit(date)
  else:
    print str(date) + ' DONT HIT GITHUB'
    datecommit(date)
