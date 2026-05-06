# 🌐 AAVA AI Web Dashboard Guide

Beautiful web interface for viewing repository analysis results on any port!

---

## 🚀 Quick Start

### Run on Default Port (8080)
```bash
python web_dashboard.py
```

### Run on Custom Port
```bash
# Port 3000
python web_dashboard.py 3000

# Port 5000
python web_dashboard.py 5000

# Port 9000
python web_dashboard.py 9000
```

### Run on Specific Host and Port
```bash
# Listen on all interfaces, port 8080
python web_dashboard.py 8080 0.0.0.0

# Listen on localhost only, port 3000
python web_dashboard.py 3000 127.0.0.1
```

---

## 📊 Access the Dashboard

After starting the server, open your browser:

```
http://localhost:8080
```

Or if using a custom port:
```
http://localhost:3000
http://localhost:5000
http://localhost:9000
```

---

## 🎯 Features

### 1. **Beautiful Visual Interface**
- Modern, responsive design
- Gradient backgrounds
- Card-based layout
- Smooth animations

### 2. **Real-time Analysis Loading**
- Load any analysis directory
- View results instantly
- No page refresh needed

### 3. **Comprehensive Statistics**
- Total files analyzed
- Languages detected
- Dependencies found
- Classes and functions count

### 4. **Detailed Sections**
- 📊 Code Structure
- 📦 Dependencies
- 📋 SDLC Artifacts
- 💡 Key Insights
- ✅ Recommendations

### 5. **Quick Access**
- Pre-loaded analysis options
- One-click loading
- Error handling

---

## 📖 Usage Examples

### Example 1: View Flask Analysis

```bash
# 1. Make sure you have Flask analysis
python main.py --repo-path flask-example --output flask-analysis

# 2. Start dashboard
python web_dashboard.py 8080

# 3. Open browser
# http://localhost:8080

# 4. Click "Load Analysis" (flask-analysis is pre-loaded)
```

### Example 2: View Multiple Analyses

```bash
# Analyze multiple repos
python main.py --repo-path flask-example --output flask-analysis
python main.py --repo-path django-example --output django-analysis
python main.py --repo-path . --output self-analysis

# Start dashboard
python web_dashboard.py 8080

# Switch between analyses in the browser
# - Enter "flask-analysis" and click Load
# - Enter "django-analysis" and click Load
# - Enter "self-analysis" and click Load
```

### Example 3: Custom Port for Team Sharing

```bash
# Run on port 3000 for team access
python web_dashboard.py 3000 0.0.0.0

# Share with team:
# http://your-ip-address:3000
```

---

## 🔧 Configuration Options

### Port Selection

| Port | Common Use |
|------|------------|
| 3000 | React/Node.js development |
| 5000 | Flask default |
| 8000 | Django default |
| 8080 | Common alternative HTTP |
| 9000 | Custom applications |

### Host Options

| Host | Description |
|------|-------------|
| `0.0.0.0` | Listen on all network interfaces (accessible from other machines) |
| `127.0.0.1` | Listen on localhost only (local access only) |
| `localhost` | Same as 127.0.0.1 |

---

## 🎨 Dashboard Sections

### 1. Header
- Title and description
- Branding

### 2. Load Analysis Section
- Input field for analysis path
- Load button
- Error messages

### 3. Available Analyses
- Quick-access cards
- Pre-configured paths
- One-click loading

### 4. Statistics Grid
- Total Files
- Languages Count
- Dependencies Count
- Classes Count
- Functions Count

### 5. Code Structure
- Classes and functions
- Imports
- Architecture patterns

### 6. Dependencies
- List of all dependencies
- Version information
- Type badges

### 7. SDLC Artifacts
- Requirements files
- Test files
- Documentation
- CI/CD configurations
- Configuration files

### 8. Key Insights
- AI-generated insights
- Project characteristics
- Quality metrics

### 9. Recommendations
- Actionable suggestions
- Improvement areas

---

## 🌐 API Endpoints

The dashboard also provides REST API endpoints:

### Get Analysis
```bash
GET /api/analysis/{path}

# Example
curl http://localhost:8080/api/analysis/flask-analysis
```

### List All Analyses
```bash
GET /api/analyses

# Example
curl http://localhost:8080/api/analyses
```

### API Documentation
```
http://localhost:8080/docs
```

---

## 💻 Command Line Options

### Basic Usage
```bash
python web_dashboard.py [PORT] [HOST]
```

### Examples
```bash
# Default (port 8080, all interfaces)
python web_dashboard.py

# Custom port
python web_dashboard.py 3000

# Custom port and host
python web_dashboard.py 5000 127.0.0.1

# Production setup
python web_dashboard.py 80 0.0.0.0
```

---

## 🔒 Security Considerations

### Local Development
```bash
# Localhost only (secure)
python web_dashboard.py 8080 127.0.0.1
```

### Team/Network Access
```bash
# All interfaces (use with caution)
python web_dashboard.py 8080 0.0.0.0
```

### Production Deployment
- Use reverse proxy (nginx, Apache)
- Enable HTTPS
- Add authentication
- Use firewall rules

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Error: Address already in use
# Solution: Use a different port
python web_dashboard.py 8081
```

### Cannot Access from Other Machines
```bash
# Make sure you're listening on 0.0.0.0
python web_dashboard.py 8080 0.0.0.0

# Check firewall settings
# Allow incoming connections on the port
```

### Analysis Not Found
```bash
# Make sure the analysis directory exists
ls -la flask-analysis/

# Check for context_map.json
ls -la flask-analysis/context_map.json

# Re-run analysis if needed
python main.py --repo-path flask-example --output flask-analysis
```

---

## 🚀 Advanced Usage

### Run in Background
```bash
# Using nohup
nohup python web_dashboard.py 8080 > dashboard.log 2>&1 &

# Using screen
screen -S dashboard
python web_dashboard.py 8080
# Press Ctrl+A, then D to detach
```

### Run with Docker
```bash
# Build image
docker build -t aava-dashboard -f Dockerfile.dashboard .

# Run container
docker run -p 8080:8080 -v $(pwd):/app aava-dashboard
```

### Run with systemd (Linux)
```bash
# Create service file
sudo nano /etc/systemd/system/aava-dashboard.service

# Add:
[Unit]
Description=AAVA AI Dashboard
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/aava-ai
ExecStart=/usr/bin/python3 web_dashboard.py 8080
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable aava-dashboard
sudo systemctl start aava-dashboard
```

---

## 📱 Mobile Access

The dashboard is responsive and works on mobile devices:

```
http://your-ip-address:8080
```

---

## 🎯 Integration Examples

### With CI/CD
```yaml
# .github/workflows/analyze.yml
- name: Run Analysis
  run: python main.py --repo-path . --output analysis

- name: Start Dashboard
  run: |
    python web_dashboard.py 8080 &
    sleep 5

- name: Take Screenshot
  run: |
    # Use puppeteer or similar
    npm install -g capture-website-cli
    capture-website http://localhost:8080 --output dashboard.png
```

### With Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name analysis.yourcompany.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Screenshots

### Main Dashboard
- Beautiful gradient header
- Statistics cards
- Analysis sections

### Loading State
- Animated spinner
- Loading message

### Results View
- Comprehensive data display
- Color-coded sections
- Easy navigation

---

## 🎨 Customization

### Change Colors
Edit `web_dashboard.py` and modify the CSS:

```css
/* Change gradient colors */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

/* Change accent color */
color: #YOUR_ACCENT_COLOR;
```

### Add Custom Sections
Add new sections in the HTML template:

```html
<div class="section">
    <h2>🎯 Your Custom Section</h2>
    <div id="customSection"></div>
</div>
```

---

## 📚 Complete Workflow

### 1. Analyze Repository
```bash
python main.py --repo-path flask-example --output flask-analysis
```

### 2. Start Dashboard
```bash
python web_dashboard.py 8080
```

### 3. Open Browser
```
http://localhost:8080
```

### 4. View Results
- Click "Load Analysis"
- Explore all sections
- Share with team

---

## 🎉 Quick Demo

```bash
# Complete demo in 3 commands

# 1. Analyze Flask
git clone --depth 1 https://github.com/pallets/flask.git flask-example
python main.py --repo-path flask-example --output flask-analysis

# 2. Start dashboard
python web_dashboard.py 8080

# 3. Open browser
# http://localhost:8080
# Click "Load Analysis" button
```

---

## 🔗 URLs Summary

| URL | Description |
|-----|-------------|
| `http://localhost:8080` | Main dashboard |
| `http://localhost:8080/docs` | API documentation |
| `http://localhost:8080/api/analysis/flask-analysis` | Flask analysis API |
| `http://localhost:8080/api/analyses` | List all analyses |

---

## ✅ Checklist

Before starting the dashboard:

- [ ] Analysis completed (`context_map.json` exists)
- [ ] Port is available
- [ ] Python dependencies installed
- [ ] Firewall allows the port (if sharing)

---

## 🎓 Tips

1. **Use port 8080** for general use (rarely conflicts)
2. **Use 127.0.0.1** for local-only access (more secure)
3. **Use 0.0.0.0** when sharing with team
4. **Keep analyses organized** in separate directories
5. **Bookmark the URL** for quick access

---

<div align="center">

**Ready to visualize your analysis?**

```bash
python web_dashboard.py 8080
```

**Then open:** http://localhost:8080

🎉 **Enjoy the beautiful dashboard!** 🎉

</div>
