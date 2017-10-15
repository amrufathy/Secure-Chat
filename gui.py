#! /usr/bin/env python

import curses
import curses.ascii
import curses.textpad
import time

import parallel
from Client import Client
from Server import Server

SERVER = 0
CLIENT = 1


def main(screen):
    set_colors(screen)
    screen.clear()
    screen.border(0)

    chat_window = make_chat_window(screen)
    text_box_window, textbox = make_chat_input_window(screen)

    _type = show_options_window(screen)

    if _type == SERVER:
        server = start_server()

        global sock
        sock = server.accept()

    elif _type == CLIENT:
        sock = Client(('127.0.0.1', 9000))
        sock.connect()

    screen.refresh()

    parallel.CursesSendThread(sock, screen, chat_window, text_box_window, textbox).start()
    parallel.CursesRecvThread(sock, screen, chat_window, text_box_window).start()

    while True:
        time.sleep(0)


def start_server():
    server = Server()
    server.start(9000)

    return server


def set_colors(screen):
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        screen.bkgd(curses.color_pair(1))


def get_host(screen):
    height, width = screen.getmaxyx()
    host_window = screen.subwin(3, 26, int(height / 2) - 1, int(width / 2) - 13)
    host_window.border(0)
    host_window.addstr(1, 1, "Host: ")
    host_window.refresh()

    curses.echo()
    curses.nocbreak()

    host = host_window.getstr(1, 7)

    curses.cbreak()
    curses.noecho()

    host_window.clear()
    screen.refresh()

    return host


def make_chat_window(screen):
    height, width = screen.getmaxyx()
    chat_window = screen.subwin(height - 4, width - 2, 1, 1)
    chat_window.scrollok(True)
    return chat_window


def make_chat_input_window(screen):
    height, width = screen.getmaxyx()
    text_box_window = screen.subwin(1, width - 25, height - 2, 1)

    textbox = curses.textpad.Textbox(text_box_window, insert_mode=True)
    curses.textpad.rectangle(screen, height - 3, 0, height - 1, width - 24)
    text_box_window.move(0, 0)
    return text_box_window, textbox


def show_options_window(screen):
    height, width = screen.getmaxyx()
    options_window = screen.subwin(6, 11, int(height / 2) - 3, int(width / 2) - 6)
    options_window.border(0)

    options_window.keypad(True)
    curses.curs_set(0)
    options_window.addstr(1, 1, "Run as:")
    pos = SERVER

    while True:
        if pos == SERVER:
            options_window.addstr(3, 2, "Server", curses.color_pair(4))
            options_window.addstr(4, 2, "Client")
        else:
            options_window.addstr(3, 2, "Server")
            options_window.addstr(4, 2, "Client", curses.color_pair(4))

        screen.refresh()
        key = options_window.getch()
        if key == curses.KEY_DOWN and pos == SERVER:
            pos = CLIENT
        elif key == curses.KEY_UP and pos == CLIENT:
            pos = SERVER
        # Enter key
        elif key == ord('\n'):
            break

    curses.curs_set(2)
    options_window.clear()
    options_window.refresh()

    return pos


curses.wrapper(main)
