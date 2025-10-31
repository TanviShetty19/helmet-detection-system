#!/usr/bin/env python3
"""
Simple web dashboard to view helmet detection results
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json
from datetime import datetime

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_dashboard_data()
        else:
            super().do_GET()
    
    def send_dashboard_data(self):
        """Send violation data as JSON"""
        violations = []
        
        # Read violation report if exists
        report_path = "data/outputs/violation_report.txt"
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                content = f.read()
                
            # Parse violations from report (simplified)
            lines = content.split('\n')
            current_violation = {}
            for line in lines:
                if 'Plate:' in line:
                    current_violation['plate'] = line.split('Plate:')[-1].strip()
                elif 'Time:' in line:
                    current_violation['time'] = line.split('Time:')[-1].strip()
                elif 'Vehicle:' in line:
                    current_violation['vehicle'] = line.split('Vehicle:')[-1].strip()
                    if current_violation:
                        violations.append(current_violation.copy())
                        current_violation = {}
        
        data = {
            'total_violations': len(violations),
            'violations': violations,
            'last_updated': datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def create_dashboard_html():
    """Create a simple HTML dashboard"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Helmet Detection Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }
        .violation { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .count { font-size: 2em; color: #e74c3c; font-weight: bold; }
        .plate { background: #f39c12; color: white; padding: 2px 8px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 Helmet Violation Detection System</h1>
        <p>Real-time monitoring of helmet compliance</p>
    </div>
    
    <div id="dashboard">
        <h2>Total Violations Detected: <span id="totalCount" class="count">0</span></h2>
        <div id="violationsList"></div>
    </div>

    <script>
        async function loadData() {
            try {
                const response = await fetch('/data');
                const data = await response.json();
                
                document.getElementById('totalCount').textContent = data.total_violations;
                
                const violationsList = document.getElementById('violationsList');
                violationsList.innerHTML = '';
                
                data.violations.forEach(violation => {
                    const div = document.createElement('div');
                    div.className = 'violation';
                    div.innerHTML = `
                        <strong>Time:</strong> ${violation.time} | 
                        <strong>Vehicle:</strong> ${violation.vehicle} | 
                        <strong>Plate:</strong> <span class="plate">${violation.plate}</span>
                    `;
                    violationsList.appendChild(div);
                });
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        // Load data every 5 seconds
        loadData();
        setInterval(loadData, 5000);
    </script>
</body>
</html>
    """
    
    with open('dashboard.html', 'w') as f:
        f.write(html)
    
    print("✅ Dashboard created: dashboard.html")

if __name__ == "__main__":
    # Create dashboard HTML
    create_dashboard_html()
    
    # Start web server
    port = 8080
    os.chdir('data/outputs')  # Serve from outputs directory
    
    print(f"🌐 Starting dashboard server at http://localhost:{port}")
    print("📊 Open the URL above to view violations dashboard")
    
    server = HTTPServer(('', port), DashboardHandler)
    server.serve_forever()