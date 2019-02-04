import curses
from curses import wrapper
from headings import Headings
import math

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

def wordwrap_text(text, line_length, num_lines):
   output_lines = []
   for i in range(0, num_lines):
      if i < (num_lines - 1):
         if(len(text) >= line_length):
            cur_line = text[:line_length]
            last_space_pos = cur_line.rfind(' ')
            cur_line  = cur_line[:last_space_pos] + (' ' * (line_length - last_space_pos))
            text = text[last_space_pos + 1:]
         else:
            cur_line = text
         output_lines.append(cur_line)
      else:
         if len(text) >= line_length:
            text = text[:line_length-3]
            last_space_pos = text.rfind(' ')
            text = text[:last_space_pos] + '...'
         output_lines.append(text)

   return ''.join(output_lines)

def draw_upcoming_events(window):
   window.clear()
   (max_y, max_x) = window.getmaxyx()

   y_pos = int(max_y / 8)
   addstr_hcenter(y_pos, "Upcoming Events", window, curses.A_BOLD | curses.A_UNDERLINE)
   y_pos += 3

   upcoming_event_retriever = UpcomingEventRetriever('https://calendar.google.com/calendar/ical/columbiagadgetworks%40gmail.com/public/basic.ics')
   for event in upcoming_event_retriever.get_upcoming_event_list(31):
      tempwin_max_y = 4
      tempwin_max_x = max_x - 4
      tempwin = window.derwin(tempwin_max_y, tempwin_max_x, y_pos, 2)
      tempwin.addstr(event.summary, curses.A_BOLD)
      tempwin.addstr(' - ')
      tempwin.addstr(event.dtstart.strftime("%A, %b %-d @ %H:%M"))
      tempwin.addstr(1, 0, wordwrap_text(event.description, tempwin_max_x, tempwin_max_y-1))

      y_pos += (tempwin_max_y + 1)

      if (tempwin_max_y + y_pos) > max_y:
         break

def main(stdscr):
   curses.curs_set(0)
   curses.mousemask(1)

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

   navwindow.timeout(3 * 60 * 1000)
   last_event = -1
   while True:
      if last_event == -1:
         draw_upcoming_events(contentwindow)

      mainwindow.refresh()

      event = navwindow.getch()
      if event == curses.KEY_MOUSE:
         curses.getmouse()
      last_event = event

wrapper(main)
