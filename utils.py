import curses
import os
import signal


def showDialog(screen, title, message, is_error):
    (height, width) = screen.getmaxyx()
    exit_message = "Press Ctrl^c to exit" if is_error else ""
    dialog_width = max(len(title), len(message), len(exit_message)) + 2
    dialog_height = 8 if message else 3
    dialog_window = screen.subwin(dialog_height, dialog_width, int(height / 2) - int(dialog_height / 2),
                                 int(width / 2) - int(dialog_width / 2))
    dialog_window.border(0)
    dialog_window.addstr(1, 1, title, curses.color_pair(2) if is_error else curses.color_pair(1))

    if message:
        dialog_window.hline(2, 1, 0, dialog_width - 2)

        dialog_window.addstr(3, 1, message)

        if is_error:
            dialog_window.addstr(6, 1, exit_message)

    curses.curs_set(0)
    dialog_window.refresh()

    if is_error:
        dialog_window.getch()
        os.kill(os.getpid(), signal.SIGINT)
    else:
        return dialog_window
