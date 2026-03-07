# chatroom-ipv6

A minimal, multi-user chat room using raw TCP over IPv6, written in Python with no external dependencies.

## Features

- IPv6-native (uses `AF_INET6` sockets)
- Multi-threaded server — each client gets its own thread
- Username prompt on join, join/leave announcements
- Broadcast to all connected users

## Requirements

- An IPv6-capable network interface (or use `::1` for localhost testing)

## Project Structure

```
chatroom-ipv6/
├── server.py   # Multi-threaded IPv6 TCP chat server
└── client.py   # Interactive CLI chat client
```

## Potential Features to Add

| Feature | Description |
|---|---|
| **Timestamps** | Prefix messages with `[HH:MM:SS]` |
| **`/users` command** | List who is currently online |
| **Private messages** | `/msg <user> <text>` for DMs |
| **Unique usernames** | Reject duplicate names on join |
| **Chat rooms/channels** | `/join <room>` to switch rooms |
| **Scrolling TUI** | `curses`-based UI so your input line doesn't mix with incoming messages |
| **Message history** | Replay the last N messages to new joiners |
| **Server log file** | Persist all messages to a dated `.log` file |
| **TLS encryption** | Wrap sockets with `ssl` for encrypted transport |
| **Dual-stack (IPv4+IPv6)** | Accept both address families |
| **Config file** | `config.ini` for port, max connections, etc. |
| **Admin commands** | `/kick <user>`, `/ban <ip>` for the server operator |
