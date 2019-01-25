import curses
from curses import wrapper
from headings import Headings

def addstr_hcenter(y_pos, message, window, attr=0):
   (max_y, max_x) = window.getmaxyx()
   x_pos = int(max((max_x / 2) - (len(message) / 2), 0))
   window.addstr(y_pos, x_pos, message, attr)

def main(stdscr):
   curses.curs_set(0)

   stdscr.clear()
   stdscr.box()
   addstr_hcenter(0, " CGW Kiosk v0.1 ", stdscr, curses.A_BOLD)
   stdscr.refresh()
   stdscr.getch()

   y_pos = 2
   for line in Headings.CGW_LOGO:
      addstr_hcenter(y_pos, line, stdscr)
      y_pos += 1

   stdscr.getch()
wrapper(main)
