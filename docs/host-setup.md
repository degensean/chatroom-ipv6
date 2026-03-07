# Host Firewall Setup

## Step 1: Set up IPv6

Follow the instructions in [ipv6-setup.md](../ipv6-setup.md).

## Step 2: Open the Firewall (Host Only)
The person running the `server.py` must allow incoming traffic.

1. In your router settings, find **Firewall**, **IPv6 Filtering**, or **Pinholing**.
2. **Create New Rule:**
   * **Service Name:** `PythonChat`
   * **Protocol:** `TCP`
   * **Port:** `5555`
   * **Local IP:** Your permanent IPv6 address from Step 1.
   * **Remote IP:** Leave blank or set to `Any` (or `::/0`).
3. **Windows Firewall (Software):**
   * If Windows blocks the connection, go to **Settings > Update & Security > Windows Security > Firewall & network protection > Allow an app through firewall** and ensure Python is checked.

---

## Step 3: Start the server

```bash
python server.py <port>
```

Listens on `::` (all IPv6 interfaces). Defaults to port `5555`.

- `host` defaults to `::1` (localhost), `port` defaults to `5555`.
- Type a message and press **Enter** to send.
- Type `QUIT` to disconnect.

### Testing locally

Run the server and one or more clients in separate terminals (defaults connect to `::1`).

