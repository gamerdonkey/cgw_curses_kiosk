
import urllib.request
from icalendar import Calendar, Event
from datetime import datetime, timedelta, timezone
from dateutil import rrule

now = datetime.now(timezone.utc)
now_plus_31_days = now + timedelta(days=31)

calendar_contents = urllib.request.urlopen("https://calendar.google.com/calendar/ical/columbiagadgetworks%40gmail.com/public/basic.ics").read()

gcal = Calendar.from_ical(calendar_contents)

events = []
for component in gcal.walk():
   if component.name == "VEVENT":
      dtstart = component.get('dtstart').dt
      if dtstart > now and dtstart < now_plus_31_days:
         events.append({'summary':component.get('summary'), 'dtstart':dtstart})
      elif component.get('RRULE'):
         rruleset = rrule.rruleset()
         rruleset.rrule( rrule.rrulestr(component.get('RRULE').to_ical().decode('utf-8'), dtstart=dtstart) )
         recurring_dates = rruleset.between(now, now_plus_31_days)
         if len(recurring_dates) > 0:
            events.append({'summary':component.get('summary'), 'dtstart':recurring_dates[0]})

for event in sorted(events, key=lambda k: k['dtstart']):
   print(event.get('summary'))
   print(event.get('dtstart'))
