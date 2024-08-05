import datetime

currentDate = datetime.date.today()

isoYear,isoWeek,isoDay = currentDate.isocalendar()

print(isoWeek)
