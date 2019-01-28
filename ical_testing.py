
import urllib.request
from icalendar import Calendar, Event
from datetime import datetime, timedelta, timezone
from dateutil import rrule

from upcomingevent import UpcomingEvent

now = datetime.now(timezone.utc)
now_plus_31_days = now + timedelta(days=31)

calendar_contents = urllib.request.urlopen("https://calendar.google.com/calendar/ical/columbiagadgetworks%40gmail.com/public/basic.ics").read()

gcal = Calendar.from_ical(calendar_contents)

events = []
for component in gcal.walk():
   if component.name == "VEVENT":
      dtstart = component.get('dtstart').dt
      if dtstart > now and dtstart < now_plus_31_days:
         event = UpcomingEvent(component.get('summary'), component.get('description', dtstart))
         events.append(event)
      elif component.get('RRULE'):
         rruleset = rrule.rruleset()
         rruleset.rrule( rrule.rrulestr(component.get('RRULE').to_ical().decode('utf-8'), dtstart=dtstart) )
         recurring_dates = rruleset.between(now, now_plus_31_days)
         if len(recurring_dates) > 0:
            event = UpcomingEvent(component.get('summary'), component.get('description'), recurring_dates[0])
            events.append(event)

for event in sorted(events, key=lambda event: event.dtstart):
   print(event.summary)
   print(event.description)
   print(event.dtstart)
