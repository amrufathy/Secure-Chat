import curses
import curses.ascii
from threading import Thread, Lock

import utils

mutex = Lock()


class CursesSendThread(Thread):
    def __init__(self, sock, screen, chat_window, text_box_window, textbox):
        self.sock = sock
        self.screen = screen
        self.chat_window = chat_window
        self.text_box_window = text_box_window
        self.textbox = textbox

        Thread.__init__(self)
        self.daemon = True

    def run(self):
        height, width = self.chat_window.getmaxyx()

        while True:
            chat_input = self.textbox.edit(self.input_validator)

            mutex.acquire()

            self.text_box_window.deleteln()
            self.text_box_window.move(0, 0)
            self.text_box_window.deleteln()
            self.chat_window.scroll(1)
            self.chat_window.addstr(height - 1, 0, chat_input[:-1], curses.color_pair(2))
            self.sock.send(chat_input[:-1])
            self.text_box_window.move(0, 0)
            self.chat_window.refresh()
            self.text_box_window.refresh()

            mutex.release()

    @staticmethod
    def input_validator(char):
        if char == curses.KEY_HOME:
            return curses.ascii.SOH
        elif char == curses.KEY_END:
            return curses.ascii.ENQ
        elif char == curses.KEY_ENTER or char == ord('\n'):
            return curses.ascii.BEL
        return char


class CursesRecvThread(Thread):
    def __init__(self, sock, screen, chat_window, text_box_window):
        self.sock = sock
        self.screen = screen
        self.chat_window = chat_window
        self.text_box_window = text_box_window

        Thread.__init__(self)
        self.daemon = True

    def run(self):
        height, width = self.chat_window.getmaxyx()

        while True:
            response = self.sock.recv()

            mutex.acquire()

            if response == "__END__":
                self.sock.disconnect()
                utils.showDialog(self.chat_window, "Connection Terminated",
                                 "The client requested to end the connection",
                                 True)

            self.chat_window.scroll(1)
            self.chat_window.addstr(height - 1, 0, response, curses.color_pair(3))
            self.text_box_window.move(0, 0)
            self.chat_window.refresh()
            self.text_box_window.refresh()

            mutex.release()
