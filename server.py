import socket
import threading
import sys
from datetime import datetime

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5555

# We will use a dictionary to keep track of clients and their usernames
clients = {}

def ts():
    """Return current time as [HH:MM:SS]."""
    return datetime.now().strftime("[%H:%M:%S]")

def broadcast(message, sender=None):
    """Sends a message to everyone except the sender."""
    for client in list(clients.keys()):
        if client != sender:
            try:
                client.send(message)
            except:
                # If a connection is broken, remove them
                client.close()
                if client in clients:
                    del clients[client]

def handle_client(client):
    try:
        # 1. Ask the user for their name as soon as they connect
        client.send("Enter your username: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8').strip()
        
        # Give them a default name if they just hit Enter
        if not username:
            username = "UnknownUser"
            
        clients[client] = username
        
        # 2. Announce to everyone that they joined
        welcome_msg = f"\n{ts()} *** {username} has joined the chat! ***\n"
        print(welcome_msg.strip()) # Print to the server console too
        broadcast(welcome_msg.encode('utf-8'), client)
        
        # 3. Listen for their messages and attach their name
        while True:
            message = client.recv(1024)
            if not message:
                break
            
            decoded_text = message.decode('utf-8').strip()
            if decoded_text == '/users':
                user_list = ', '.join(clients.values())
                client.send(f"{ts()} Online: {user_list}\n".encode('utf-8'))
            elif decoded_text:
                formatted_message = f"{ts()} [{username}]: {decoded_text}\n"
                broadcast(formatted_message.encode('utf-8'), client)
                
    except:
        pass
    finally:
        # 4. Announce when they leave
        if client in clients:
            user = clients[client]
            del clients[client]
            leave_msg = f"\n{ts()} *** {user} has left the chat. ***\n"
            print(leave_msg.strip())
            broadcast(leave_msg.encode('utf-8'))
        client.close()

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('::', PORT))
server.listen()
server.settimeout(1.0)

print(f"IPv6 Chat Server running on port {PORT}. Press Ctrl+C to stop.")

try:
    while True:
        try:
            client, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
            thread.start()
        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server.close()
    sys.exit(0)
