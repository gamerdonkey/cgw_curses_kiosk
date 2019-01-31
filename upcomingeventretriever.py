
import urllib.request
from icalendar import Calendar, Event
from datetime import datetime, timedelta, timezone
from dateutil import rrule
from upcomingevent import UpcomingEvent

class UpcomingEventRetriever:
   'Retrieves upcoming events from an icalendar url'

   def __init__(self, icalendar_url):
      self.icalendar_url = icalendar_url
      self.refresh_calendar()

   def refresh_calendar(self):
      calendar_contents = urllib.request.urlopen(self.icalendar_url).read()
      self.calendar = Calendar.from_ical(calendar_contents)

   def get_upcoming_event_list(self, timedelta_in_days):
      now = datetime.now(timezone.utc)
      end_date = now + timedelta(days=timedelta_in_days)

      events = []
      for component in self.calendar.walk():
         if component.name == "VEVENT":
            summary = component.get('summary')
            description = component.get('description')
            dtstart = component.get('dtstart').dt
            if dtstart > now and dtstart < end_date:
               events.append(UpcomingEvent(summary, description, dtstart))
            elif component.get('RRULE'):
               rruleset = rrule.rruleset()
               rruleset.rrule( rrule.rrulestr(component.get('RRULE').to_ical().decode('utf-8'), dtstart=dtstart) )
               recurring_dates = rruleset.between(now, end_date)
               if len(recurring_dates) > 0:
                  events.append(UpcomingEvent(summary, description, recurring_dates[0]))

      return sorted(events, key=lambda event: event.dtstart)
