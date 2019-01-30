import curses
from curses import wrapper
from headings import Headings

def addstr_hcenter(y_pos, message, window, attr=0):
   (max_y, max_x) = window.getmaxyx()
   x_pos = int(max((max_x / 2) - (len(message) / 2), 0))
   window.addstr(y_pos, x_pos, message, attr)

def draw_heading(heading, window):
   y_pos = 0
   for line in heading:
      addstr_hcenter(y_pos, line, window)
      y_pos += 1

def main(stdscr):
   curses.curs_set(0)

   stdscr.clear()
   stdscr.box()
   addstr_hcenter(0, " CGW Kiosk v0.1 ", stdscr, curses.A_BOLD)
   stdscr.refresh()

   mainwindow = stdscr.derwin(curses.LINES - 2, curses.COLS - 2, 1, 1)

   headingwindow = mainwindow.derwin(len(Headings.CGW_LOGO) + 1, curses.COLS - 2, 0, 0)

   draw_heading(Headings.CGW_LOGO, headingwindow)

   upcomingeventswindow = mainwindow.derwin(10, curses.COLS -2, len(Headings.CGW_LOGO) + 2, 0)
   upcomingeventswindow.box()

   mainwindow.getch()

wrapper(main)
