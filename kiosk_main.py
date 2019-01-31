import curses
from curses import wrapper
from headings import Headings

from upcomingeventretriever import UpcomingEventRetriever

def addstr_hcenter(y_pos, message, window, attr=0):
   (max_y, max_x) = window.getmaxyx()
   x_pos = int(max((max_x / 2) - (len(message) / 2), 0))
   window.addstr(y_pos, x_pos, message, attr)

def draw_heading(heading, window):
   y_pos = 0
   for line in heading:
      addstr_hcenter(y_pos, line, window)
      y_pos += 1

def draw_upcoming_events(window):
   window.clear()
   (max_y, max_x) = window.getmaxyx()

   y_pos = int(max_y / 8)
   addstr_hcenter(y_pos, "Upcoming Events", window, curses.A_BOLD | curses.A_UNDERLINE)
   y_pos += 3

   upcoming_event_retriever = UpcomingEventRetriever('https://calendar.google.com/calendar/ical/columbiagadgetworks%40gmail.com/public/basic.ics')
   for event in upcoming_event_retriever.get_upcoming_event_list(31):
      tempwin_max_y = 3
      tempwin_max_x = max_x - 4
      tempwin = window.derwin(tempwin_max_y, tempwin_max_x, y_pos, 2)
      tempwin.addstr(event.summary, curses.A_BOLD)
      tempwin.addstr(' - ')
      tempwin.addstr(event.dtstart.strftime("%A, %b %-d @ %H:%M"))
      tempwin.addstr(1, 0, event.description[:2*tempwin_max_x-1])

      y_pos += 4

def main(stdscr):
   curses.curs_set(0)

   stdscr.clear()
   stdscr.box()
   addstr_hcenter(0, " CGW Kiosk v0.1 ", stdscr, curses.A_BOLD)
   stdscr.refresh()

   mainwindow = stdscr.derwin(curses.LINES - 2, curses.COLS - 2, 1, 1)

   (mainwindow_height, mainwindow_width) = mainwindow.getmaxyx()

   headingwindow_height = len(Headings.CGW_LOGO) + 1
   headingwindow = mainwindow.derwin(headingwindow_height, mainwindow_width, 0, 0)

   draw_heading(Headings.CGW_LOGO, headingwindow)

   navwindow_height = 14
   navwindow = mainwindow.derwin(navwindow_height, mainwindow_width, mainwindow_height - navwindow_height, 0)
   navwindow.box()

   contentwindow_height = mainwindow_height - (headingwindow_height + navwindow_height)
   contentwindow = mainwindow.derwin(contentwindow_height, mainwindow_width, headingwindow_height, 0)

   draw_upcoming_events(contentwindow)

   mainwindow.getch()

wrapper(main)
