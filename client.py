import socket
import threading
import sys

# The host's public IPv6 address goes here. 
# (Use '::1' if you are testing this on the same computer as the server)
HOST_IPV6 = '::1' 
PORT = 5555

def receive_messages(sock):
    while True:
        try:
            # Listen for incoming messages
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("\nConnection closed by the server.")
            break
    sock.close()
    sys.exit(0)

try:
    # Set up the IPv6 connection
    client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client.connect((HOST_IPV6, PORT))
    print(f"Successfully connected to the chat! Type a message and hit Enter.")
    print("Type 'QUIT' to exit.\n" + "-"*40)
    
    # Start a background task to constantly listen for friends' messages
    thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    thread.start()

    # The main loop lets you type and send messages
    while True:
        msg = input()
        if msg.strip().upper() == 'QUIT':
            break
        # Send your message to the server
        client.send(msg.encode('utf-8'))

except Exception as e:
    print(f"Could not connect: {e}")
finally:
    client.close()
