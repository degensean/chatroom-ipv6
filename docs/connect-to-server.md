# Connect to Server

## Step 1: Set up IPv6

Follow the instructions in [ipv6-setup.md](../ipv6-setup.md).

## Step 2: Connect to Server

### Method 1 (has UI, recommended)

Windows does not have `nc` by default. It is recommended to use the `client.py` script provided, as many nc.exe downloads are flagged by antivirus software.

```bash
python client.py <server_ipv6> <port>
```

### Method 2 (very basic, works on Linux/Mac)

```bash
sudo apt update && sudo apt install netcat-openbsd -y # Linux
brew install netcat # macOS
```

Connect to the server:

```bash
nc -6 <server_ipv6> <port>
```

