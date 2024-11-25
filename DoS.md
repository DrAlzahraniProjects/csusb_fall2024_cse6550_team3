# **Denial of Service (DoS) Protection**

Denial of Service (DoS) attacks overwhelm a target system with a flood of illegitimate requests, preventing legitimate users from accessing services. This guide provides an implementation plan for protecting applications from DoS attacks using **rate limiting**, **IP blacklisting**, **traffic filtering**, and **monitoring**.

---

## **Table of Contents**
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)
6. [Conclusion](#conclusion)

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/dos-protection.git
cd dos-protection
```

### **2. Install Dependencies**

Install the required libraries based on the technology used:

#### **For Python with Flask:**
```bash
# Install Flask and Flask-Limiter
pip install flask flask-limiter
```

#### **Network Security Tools:**
- **`iptables`**: Used for configuring firewall rules.
- **`Fail2Ban`**: Monitors logs and bans suspicious IPs.

```bash
# Install iptables
sudo apt-get install iptables

# Install Fail2Ban
sudo apt-get install fail2ban
```

---

## **Configuration**

### **Rate Limiting Configuration**

Rate limiting controls the number of requests from each IP, preventing DoS attacks by throttling requests.

#### **Example: Flask with `flask-limiter`**
```python
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Set up rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Use remote IP address to limit
    default_limits=["100 per minute"]  # Default limit for all routes
)

@app.route("/api")
@limiter.limit("50 per minute")  # Limit /api endpoint to 50 requests per minute per IP
def api():
    return "This is a rate-limited API endpoint"

if __name__ == "__main__":
    app.run()
```

This configuration limits the `/api` endpoint to 50 requests per minute from a single IP address.

### **IP Blacklisting Configuration**

To block repeat offenders, use `iptables` to blacklist specific IP addresses.

```bash
# Block a specific IP address
sudo iptables -A INPUT -s 192.168.0.1 -j DROP

# Verify the blocked IPs
sudo iptables -L
```

To block an IP after repeated failed attempts, use `Fail2Ban`:

#### **Example: Configure Fail2Ban for SSH**
Edit the `jail.local` file:

```bash
sudo vim /etc/fail2ban/jail.local
```

Add the following configuration:

```ini
[sshd]
enabled = true
maxretry = 3
bantime = 3600
findtime = 600
logpath = /var/log/auth.log
```

- **`maxretry`**: Number of failed attempts before banning.
- **`bantime`**: Ban duration in seconds.

### **Traffic Filtering Configuration**

Deep packet inspection tools like `Suricata` help filter suspicious traffic patterns.

```bash
# Install Suricata
sudo apt-get install suricata

# Run Suricata for Real-time Traffic Filtering
sudo suricata -c /etc/suricata/suricata.yaml -i eth0
```

This inspects traffic in real-time and blocks abnormal or malicious traffic.

---

## **Implementation**

### **Step 1: Implementing Rate Limiting in Flask**
```python
from flask import Flask
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/data")
@limiter.limit("100 per minute")  # Limit to 100 requests per minute per IP
def get_data():
    return "This route is protected with rate limiting."

if __name__ == "__main__":
    app.run()
```

### **Step 2: Configuring Firewall Rules**

For higher-level DoS protection, configure firewall rules using `iptables`.

```bash
# Block traffic from a specific malicious IP
sudo iptables -A INPUT -s 203.0.113.45 -j DROP
```

### **Step 3: Logging and Monitoring**

To protect services like SSH from brute-force attacks, use `Fail2Ban` to monitor logs and ban suspicious IPs.

```bash
# Start Fail2Ban service
sudo service fail2ban start

# View Fail2Ban log to verify bans
sudo tail -f /var/log/fail2ban.log
```

Configure the `jail.local` file to monitor SSH or HTTP and automatically block malicious IPs.

---

## **Usage**

After configuring your application and security tools:

1. **Run the Flask Application:**
   ```bash
   python app.py
   ```

2. **Ensure `Fail2Ban` and `Suricata` Are Running:**
   ```bash
   sudo service fail2ban start
   sudo suricata -c /etc/suricata/suricata.yaml -i eth0
   ```

Your application is now equipped to handle potential DoS attacks with rate limiting, IP blacklisting, and traffic filtering.

---

## **Troubleshooting**

- **Rate Limiting Issues**: If legitimate users are blocked, adjust limits in the Flask application or check logs for blocking reasons.
- **Firewall Not Blocking IPs**: Ensure `iptables` rules are correctly set. Verify with:
   ```bash
   sudo iptables -L
   ```
- **Fail2Ban Not Working**: Confirm the service is running and check logs for errors:
   ```bash
   sudo tail -f /var/log/fail2ban.log
   ```
- **Suricata Performance**: If Suricata impacts performance, optimize its configuration and adjust resource limits.

---

## **Conclusion**

This project offers a layered approach to DoS protection by combining rate limiting, IP blacklisting, traffic filtering, and logging. Properly configuring these tools can help secure your infrastructure against various forms of malicious activity.
