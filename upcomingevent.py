class UpcomingEvent:
   'Simple data container for upcoming calendar events'

   def __init__(self, summary, description, dtstart):
      self.summary = summary
      self.description = description
      self.dtstart = dtstart
