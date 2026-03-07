# 🌐 Direct P2P Chat via IPv6: The Setup Guide

This guide helps you establish a direct, service-free terminal chat using your computer's native IPv6 capabilities. This method bypasses central servers by using the public internet as a direct bridge.

---

## 🛠 Step 1: Check Your IPv6 Status
Before starting, every participant must verify they have a **Global Unicast Address** (a public IPv6 address).

### **Windows**
1. Open **Command Prompt**.
2. Type `ipconfig | grep IPv6`.
3. Look for **IPv6 Address** (typically starts with `2` or `3`).
   * *Note: If you only see `fe80::`, your network is not currently providing public IPv6.*

### **macOS / Linux**
1. Open **Terminal**.
2. Run: `ip addr` (Linux) or `ifconfig` (macOS).
3. Look for the `inet6` entry under your active interface (e.g., `eth0` or `en0`) that says `scope global`.
   * **Quick Test:** Run `curl -6 icanhazip.com`. If it returns an address, you are ready! Otherwise, follow Step 2.

---

## ⚙️ Step 2: Enable IPv6 on Your Router
If Step 1 failed, your router likely has IPv6 disabled.

1. **Access Admin Panel:** Open your browser and go to your router's admin panel (You can find this on the back of your router, e.g., `http://router.asus.com`).
2. **Login:** Use the admin credentials on the back of your router.
3. **Navigate to IPv6:** Look for "Advanced Settings," "Internet," or "WAN."
4. **Configuration:**
   * **Connection Type:** Set to **Native** (or DHCPv6).
   * **Auto Configuration:** Set to **Stateless** (SLAAC).
   * **Router Advertisement:** Set to **Enable**.
5. **Save & Apply:** Wait 1 minute and re-run the check in Step 1.
