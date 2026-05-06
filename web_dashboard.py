#!/usr/bin/env python3
"""
AAVA AI Web Dashboard
Beautiful web interface for viewing repository analysis results
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from typing import Optional
import uvicorn
import os

app = FastAPI(
    title="AAVA AI Dashboard",
    description="Web Dashboard for Repository Analysis",
    version="1.0.0"
)

# Store for analysis results
analysis_cache = {}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AAVA AI - Repository Analysis Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .upload-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .upload-section h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .results-section {
            display: none;
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .results-section.active {
            display: block;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: bold;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .list-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .error.active {
            display: block;
        }
        
        .available-analyses {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .analysis-card {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .analysis-card:hover {
            transform: translateX(5px);
            background: #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AAVA AI Dashboard</h1>
            <p>HP SDLC Agentic AI - Repository Analysis & Contextualization</p>
        </div>
        
        <div class="upload-section">
            <h2>📊 Load Analysis Results</h2>
            <div class="error" id="error"></div>
            <div class="form-group">
                <label for="analysisPath">Analysis Directory Path:</label>
                <input type="text" id="analysisPath" placeholder="e.g., flask-analysis or output" value="flask-analysis">
            </div>
            <button class="btn" onclick="loadAnalysis()">Load Analysis</button>
        </div>
        
        <div class="available-analyses">
            <h2>📁 Available Analyses</h2>
            <div id="availableList">
                <div class="analysis-card" onclick="document.getElementById('analysisPath').value='output'; loadAnalysis();">
                    <strong>output/</strong> - Self-analysis of AAVA AI
                </div>
                <div class="analysis-card" onclick="document.getElementById('analysisPath').value='flask-analysis'; loadAnalysis();">
                    <strong>flask-analysis/</strong> - Flask Web Framework
                </div>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Loading analysis results...</p>
        </div>
        
        <div class="results-section" id="results">
            <h2>📈 Analysis Results</h2>
            
            <div class="stats-grid" id="statsGrid"></div>
            
            <div class="section">
                <h2>🏗️ Code Structure</h2>
                <div id="structure"></div>
            </div>
            
            <div class="section">
                <h2>📦 Dependencies</h2>
                <div id="dependencies"></div>
            </div>
            
            <div class="section">
                <h2>📋 SDLC Artifacts</h2>
                <div id="artifacts"></div>
            </div>
            
            <div class="section">
                <h2>💡 Key Insights</h2>
                <div id="insights"></div>
            </div>
            
            <div class="section">
                <h2>✅ Recommendations</h2>
                <div id="recommendations"></div>
            </div>
        </div>
    </div>
    
    <script>
        async function loadAnalysis() {
            const path = document.getElementById('analysisPath').value;
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const error = document.getElementById('error');
            
            // Show loading
            loading.classList.add('active');
            results.classList.remove('active');
            error.classList.remove('active');
            
            try {
                const response = await fetch(`/api/analysis/${encodeURIComponent(path)}`);
                
                if (!response.ok) {
                    throw new Error('Analysis not found. Make sure the path is correct.');
                }
                
                const data = await response.json();
                displayResults(data);
                
                // Hide loading, show results
                loading.classList.remove('active');
                results.classList.add('active');
                
            } catch (err) {
                loading.classList.remove('active');
                error.textContent = err.message;
                error.classList.add('active');
            }
        }
        
        function displayResults(data) {
            // Stats Grid
            const statsGrid = document.getElementById('statsGrid');
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <h3>Total Files</h3>
                    <div class="value">${data.total_files}</div>
                </div>
                <div class="stat-card">
                    <h3>Languages</h3>
                    <div class="value">${data.languages.length}</div>
                </div>
                <div class="stat-card">
                    <h3>Dependencies</h3>
                    <div class="value">${data.dependencies.length}</div>
                </div>
                <div class="stat-card">
                    <h3>Classes</h3>
                    <div class="value">${data.structure.statistics.total_classes || 0}</div>
                </div>
                <div class="stat-card">
                    <h3>Functions</h3>
                    <div class="value">${data.structure.statistics.total_functions || 0}</div>
                </div>
            `;
            
            // Structure
            const structure = document.getElementById('structure');
            structure.innerHTML = `
                <div class="list-item">
                    <strong>Classes:</strong> ${data.structure.statistics.total_classes || 0}<br>
                    <strong>Functions:</strong> ${data.structure.statistics.total_functions || 0}<br>
                    <strong>Imports:</strong> ${data.structure.imports.length}<br>
                    <strong>Architecture Patterns:</strong> ${data.structure.architecture_patterns.join(', ') || 'None detected'}
                </div>
            `;
            
            // Dependencies
            const dependencies = document.getElementById('dependencies');
            dependencies.innerHTML = data.dependencies.slice(0, 10).map(dep => `
                <div class="list-item">
                    <strong>${dep.name}</strong> 
                    <span class="badge">${dep.type}</span>
                    ${dep.version ? `<span class="badge">${dep.version}</span>` : ''}
                </div>
            `).join('') + (data.dependencies.length > 10 ? `<p>... and ${data.dependencies.length - 10} more</p>` : '');
            
            // SDLC Artifacts
            const artifacts = document.getElementById('artifacts');
            let artifactsHtml = '';
            for (const [type, items] of Object.entries(data.sdlc_artifacts)) {
                if (type !== 'test_coverage' && Array.isArray(items)) {
                    artifactsHtml += `
                        <div class="list-item">
                            <strong>${type.replace('_', ' ').toUpperCase()}:</strong> ${items.length} files
                        </div>
                    `;
                }
            }
            artifacts.innerHTML = artifactsHtml;
            
            // Insights
            const insights = document.getElementById('insights');
            insights.innerHTML = data.insights.map(insight => `
                <div class="list-item">💡 ${insight}</div>
            `).join('');
            
            // Recommendations
            const recommendations = document.getElementById('recommendations');
            recommendations.innerHTML = data.recommendations.map((rec, idx) => `
                <div class="list-item">✅ ${idx + 1}. ${rec}</div>
            `).join('');
        }
        
        // Auto-load if flask-analysis exists
        window.onload = function() {
            // Try to load flask-analysis by default
            setTimeout(() => {
                loadAnalysis();
            }, 500);
        };
    </script>
</body>
</html>
    """
    
    return HTMLResponse(content=html_content)


@app.get("/api/analysis/{path:path}")
async def get_analysis(path: str):
    """Get analysis results from a directory"""
    
    # Construct path to context_map.json
    context_file = Path(path) / "context_map.json"
    
    if not context_file.exists():
        raise HTTPException(status_code=404, detail=f"Analysis not found at {path}")
    
    try:
        with open(context_file, 'r') as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading analysis: {str(e)}")


@app.get("/api/analyses")
async def list_analyses():
    """List all available analyses"""
    
    analyses = []
    
    # Look for directories with context_map.json
    for item in Path('.').iterdir():
        if item.is_dir():
            context_file = item / "context_map.json"
            if context_file.exists():
                try:
                    with open(context_file, 'r') as f:
                        data = json.load(f)
                    analyses.append({
                        'path': str(item),
                        'name': data.get('repository_name', item.name),
                        'files': data.get('total_files', 0),
                        'timestamp': data.get('timestamp', '')
                    })
                except:
                    pass
    
    return JSONResponse(content=analyses)


def run_dashboard(host: str = "0.0.0.0", port: int = 8080):
    """Run the dashboard server"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 AAVA AI Dashboard Starting...                  ║
║                                                              ║
║  Dashboard URL: http://{host}:{port}                    ║
║  API Docs: http://{host}:{port}/docs                    ║
║                                                              ║
║  Press Ctrl+C to stop the server                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    port = 8080
    host = "0.0.0.0"
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    run_dashboard(host=host, port=port)
