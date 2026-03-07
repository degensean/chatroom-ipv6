import socket
import threading
import sys
import curses
from datetime import datetime

# Usage: python client.py [host] [port]
# Defaults to ::1 (localhost) on port 5555
HOST_IPV6 = sys.argv[1] if len(sys.argv) > 1 else '::1'
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5555


def chat_ui(stdscr, client, username):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    # Top area: scrolling message history
    msg_win = curses.newwin(height - 2, width, 0, 0)
    # Middle: separator / status bar
    sep_win = curses.newwin(1, width, height - 2, 0)
    # Bottom: input line
    inp_win = curses.newwin(1, width, height - 1, 0)

    msg_win.scrollok(True)

    status = f' {username}  |  /users  |  QUIT to exit '
    sep_win.bkgd(' ', curses.A_REVERSE)
    sep_win.addstr(0, 0, status[:width - 1])
    sep_win.refresh()

    lock = threading.Lock()
    prompt = f'[{username}]> '
    buf = []

    def redraw_input():
        """Redraw the input line (must be called with lock held)."""
        inp_win.clear()
        line = prompt + ''.join(buf)
        inp_win.addstr(0, 0, line[:width - 1])
        inp_win.move(0, min(len(prompt) + len(buf), width - 1))
        inp_win.refresh()

    def add_message(msg):
        with lock:
            for line in msg.splitlines():
                if line:
                    msg_win.addstr(line + '\n')
            msg_win.refresh()
            redraw_input()  # restore cursor to input window

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
                if msg:
                    add_message(msg)
                else:
                    add_message('\nDisconnected from server.')
                    break
            except:
                add_message('\nConnection closed.')
                break

    threading.Thread(target=receive, daemon=True).start()

    inp_win.keypad(True)
    with lock:
        redraw_input()

    while True:
        ch = inp_win.get_wch()

        if ch in ('\n', '\r', curses.KEY_ENTER):
            with lock:
                msg = ''.join(buf)
                buf.clear()
                if msg.strip().upper() == 'QUIT':
                    break
                if msg.strip():
                    client.send(msg.encode('utf-8'))
                    ts = datetime.now().strftime("[%H:%M:%S]")
                    msg_win.addstr(f"{ts} [{username}]: {msg}\n")
                    msg_win.refresh()
                redraw_input()

        elif ch in (curses.KEY_BACKSPACE, '\x7f', '\b'):
            with lock:
                if buf:
                    buf.pop()
                redraw_input()

        elif isinstance(ch, str) and ch.isprintable():
            with lock:
                buf.append(ch)
                redraw_input()

        elif isinstance(ch, int) and 32 <= ch < 256:
            with lock:
                buf.append(chr(ch))
                redraw_input()


try:
    client_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_sock.connect((HOST_IPV6, PORT))

    # Handle the username prompt synchronously before entering the TUI
    server_prompt = client_sock.recv(1024).decode('utf-8')
    username = input(server_prompt).strip() or 'UnknownUser'
    client_sock.send(username.encode('utf-8'))

    curses.wrapper(lambda stdscr: chat_ui(stdscr, client_sock, username))

except Exception as e:
    print(f'Could not connect: {e}')
finally:
    try:
        client_sock.close()
    except NameError:
        pass
