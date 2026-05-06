# 🌐 Running AAVA AI on Different Ports - Quick Reference

## 🚀 One-Line Commands

### Default Port (8080)
```bash
python web_dashboard.py
```
**Access:** http://localhost:8080

---

### Port 3000 (React/Node.js Style)
```bash
python web_dashboard.py 3000
```
**Access:** http://localhost:3000

---

### Port 5000 (Flask Style)
```bash
python web_dashboard.py 5000
```
**Access:** http://localhost:5000

---

### Port 8000 (Django Style)
```bash
python web_dashboard.py 8000
```
**Access:** http://localhost:8000

---

### Port 9000 (Custom)
```bash
python web_dashboard.py 9000
```
**Access:** http://localhost:9000

---

### Port 80 (HTTP Standard - Requires sudo)
```bash
sudo python web_dashboard.py 80
```
**Access:** http://localhost

---

## 🌍 Network Access (Share with Team)

### Allow Access from Other Computers
```bash
python web_dashboard.py 8080 0.0.0.0
```
**Access from other machines:** http://YOUR_IP:8080

### Find Your IP Address
```bash
# macOS/Linux
ifconfig | grep "inet "

# Or
hostname -I
```

---

## 🎯 Complete Examples

### Example 1: Quick Local Demo
```bash
# Start on port 8080
python web_dashboard.py 8080

# Open browser
open http://localhost:8080
```

### Example 2: Team Sharing
```bash
# Start on port 3000, accessible from network
python web_dashboard.py 3000 0.0.0.0

# Share this URL with team
echo "Dashboard: http://$(hostname -I | awk '{print $1}'):3000"
```

### Example 3: Multiple Dashboards
```bash
# Terminal 1: Flask analysis on port 8080
python web_dashboard.py 8080

# Terminal 2: Django analysis on port 8081
python web_dashboard.py 8081

# Terminal 3: React analysis on port 8082
python web_dashboard.py 8082
```

---

## 📊 Port Comparison

| Port | Command | Best For | Access URL |
|------|---------|----------|------------|
| 3000 | `python web_dashboard.py 3000` | React devs | http://localhost:3000 |
| 5000 | `python web_dashboard.py 5000` | Flask devs | http://localhost:5000 |
| 8000 | `python web_dashboard.py 8000` | Django devs | http://localhost:8000 |
| 8080 | `python web_dashboard.py 8080` | General use | http://localhost:8080 |
| 9000 | `python web_dashboard.py 9000` | Custom apps | http://localhost:9000 |

---

## 🔧 Troubleshooting

### Port Already in Use?
```bash
# Try next port
python web_dashboard.py 8081

# Or find what's using the port
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Can't Access from Other Machines?
```bash
# Make sure you're using 0.0.0.0
python web_dashboard.py 8080 0.0.0.0

# Check firewall
# macOS: System Preferences > Security > Firewall
# Linux: sudo ufw allow 8080
```

---

## 🎨 Visual Guide

```
┌─────────────────────────────────────────────┐
│  Your Computer                              │
│                                             │
│  python web_dashboard.py 8080               │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  AAVA AI Dashboard                  │   │
│  │  Running on port 8080               │   │
│  │                                     │   │
│  │  http://localhost:8080              │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
         │
         │ Browser Access
         ▼
┌─────────────────────────────────────────────┐
│  Web Browser                                │
│                                             │
│  [http://localhost:8080]                    │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  🚀 AAVA AI Dashboard               │   │
│  │  ═══════════════════════════════    │   │
│  │                                     │   │
│  │  📊 Statistics                      │   │
│  │  📦 Dependencies                    │   │
│  │  💡 Insights                        │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Workflow

### Step 1: Analyze a Repository
```bash
python main.py --repo-path flask-example --output flask-analysis
```

### Step 2: Start Dashboard on Your Preferred Port
```bash
# Choose one:
python web_dashboard.py 3000   # React style
python web_dashboard.py 5000   # Flask style
python web_dashboard.py 8000   # Django style
python web_dashboard.py 8080   # Default
```

### Step 3: Open Browser
```bash
# Automatically open browser (macOS)
open http://localhost:8080

# Or manually navigate to:
# http://localhost:YOUR_PORT
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Developer Workstation
```bash
# Use familiar port
python web_dashboard.py 3000

# Access locally
http://localhost:3000
```

### Scenario 2: Team Demo
```bash
# Share with team
python web_dashboard.py 8080 0.0.0.0

# Team accesses via
http://192.168.1.100:8080
```

### Scenario 3: CI/CD Integration
```bash
# Run on standard port
python web_dashboard.py 8080

# Screenshot for reports
curl http://localhost:8080 > dashboard.html
```

### Scenario 4: Multiple Projects
```bash
# Project A
python web_dashboard.py 8080 &

# Project B
python web_dashboard.py 8081 &

# Project C
python web_dashboard.py 8082 &
```

---

## 📱 Access from Mobile

### Same Network
```bash
# Start with network access
python web_dashboard.py 8080 0.0.0.0

# On mobile browser, visit:
http://YOUR_COMPUTER_IP:8080
```

---

## 🔒 Security Tips

### Local Development (Secure)
```bash
# Localhost only
python web_dashboard.py 8080 127.0.0.1
```

### Team Access (Use with Caution)
```bash
# All interfaces
python web_dashboard.py 8080 0.0.0.0

# Consider:
# - Use VPN
# - Add authentication
# - Use HTTPS
# - Firewall rules
```

---

## ✅ Checklist

Before starting:
- [ ] Analysis completed
- [ ] Port available
- [ ] Dependencies installed
- [ ] Know your access URL

---

## 🎉 Success!

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 AAVA AI Dashboard Starting...                  ║
║                                                              ║
║  Dashboard URL: http://0.0.0.0:8080                    ║
║  API Docs: http://0.0.0.0:8080/docs                    ║
║                                                              ║
║  Press Ctrl+C to stop the server                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

<div align="center">

**Choose Your Port and Start!**

```bash
python web_dashboard.py YOUR_PORT
```

**Then visit:** http://localhost:YOUR_PORT

🎨 **Beautiful Dashboard Awaits!** 🎨

</div>
