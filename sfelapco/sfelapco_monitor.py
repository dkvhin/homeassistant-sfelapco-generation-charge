#!/usr/bin/env python3
"""
SFELAPCO Generation Charge Monitor
Scrapes generation charge data from SFELAPCO website and provides it to Home Assistant
"""

import os
import re
import json
import time
import logging
import schedule
import requests
import sys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SFELAPCOMonitor:
    def __init__(self):
        self.url = "https://sfelapco.com/content.php?content_id=302"
        self.data_file = "/data/sfelapco_data.json"
        self.current_charge = None
        self.charge_history = []
        self.last_update = None
        
        # Configuration from environment variables
        self.update_interval_days = float(os.getenv('UPDATE_INTERVAL', 1.0))  # Default: 1 day
        self.retain_history = os.getenv('RETAIN_HISTORY', 'true').lower() == 'true'
        self.max_history_days = int(os.getenv('MAX_HISTORY_DAYS', 365))
        
        # Load existing data
        self.load_data()
        
    def load_data(self):
        """Load existing data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.current_charge = data.get('current_charge')
                    self.charge_history = data.get('charge_history', [])
                    self.last_update = data.get('last_update')
                    logger.info(f"Loaded {len(self.charge_history)} historical records")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            
    def save_data(self):
        """Save data to file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = {
                'current_charge': self.current_charge,
                'charge_history': self.charge_history,
                'last_update': self.last_update
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            
    def scrape_generation_charge(self):
        """Scrape generation charge from SFELAPCO website"""
        try:
            logger.info("Fetching data from SFELAPCO website...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for generation charge text
            text_content = soup.get_text()
            
            # Extract current generation charges using regex
            # Pattern: Month Year: Php X.XXXXX
            pattern = r'(\w{3})\.\s*(\d{4}):\s*Php\s*([\d.]+)'
            matches = re.findall(pattern, text_content)
            
            if matches:
                # Get the most recent charge (first match)
                month_abbr, year, rate = matches[0]
                
                # Convert month abbreviation to full name
                month_map = {
                    'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                    'Apr': 'April', 'May': 'May', 'Jun': 'June',
                    'Jul': 'July', 'Aug': 'August', 'Sep': 'September',
                    'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
                }
                
                month = month_map.get(month_abbr, month_abbr)
                
                new_charge = {
                    'month': month,
                    'year': int(year),
                    'rate': float(rate),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Update current charge
                old_charge = self.current_charge
                self.current_charge = new_charge
                self.last_update = datetime.now().isoformat()
                
                # Add to history if it's a new entry
                if self.retain_history:
                    # Check if this month/year combination already exists
                    existing = next((item for item in self.charge_history 
                                   if item['month'] == month and item['year'] == int(year)), None)
                    
                    if not existing:
                        self.charge_history.append(new_charge)
                        logger.info(f"Added new charge to history: {month} {year} - {rate} PHP/kWh")
                    elif existing['rate'] != float(rate):
                        # Update existing entry if rate changed
                        existing['rate'] = float(rate)
                        existing['timestamp'] = datetime.now().isoformat()
                        logger.info(f"Updated charge: {month} {year} - {rate} PHP/kWh")
                
                # Clean old history
                if self.retain_history and self.max_history_days > 0:
                    cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
                    self.charge_history = [
                        item for item in self.charge_history
                        if datetime.fromisoformat(item['timestamp']) > cutoff_date
                    ]
                
                # Save data
                self.save_data()
                
                if old_charge != new_charge:
                    logger.info(f"New generation charge: {month} {year} - {rate} PHP/kWh")
                else:
                    logger.info(f"Generation charge unchanged: {month} {year} - {rate} PHP/kWh")
                
                return True
                
            else:
                logger.warning("No generation charge data found on website")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Network error fetching data: {e}")
            return False
        except Exception as e:
            logger.error(f"Error scraping generation charge: {e}")
            return False
    
    def get_status(self):
        """Get current status for web interface"""
        return {
            'current_charge': self.current_charge,
            'last_update': self.last_update,
            'history_count': len(self.charge_history),
            'update_interval_days': self.update_interval_days,
            'retain_history': self.retain_history,
            'max_history_days': self.max_history_days
        }
    
    def get_history(self):
        """Get charge history"""
        return sorted(self.charge_history, key=lambda x: (x['year'], x['month']), reverse=True)

# Flask web interface
from flask import Flask, render_template, jsonify, request, abort
app = Flask(__name__, template_folder='/web/templates', static_folder='/web/static')
monitor = SFELAPCOMonitor()

# Ingress security: Only allow connections from Home Assistant ingress gateway or localhost
@app.before_request
def limit_remote_addr():
    # Log request details for debugging
    logger.debug(f"Request from {request.environ.get('REMOTE_ADDR')} to {request.path}")
    
    # Allow connections from:
    # - Home Assistant ingress gateway IP (172.30.32.2)
    # - Localhost (127.0.0.1, ::1) for direct API access
    # - Home Assistant supervisor network (172.30.32.0/24)
    client_ip = request.environ.get('REMOTE_ADDR')
    allowed_ips = ['172.30.32.2', '127.0.0.1', '::1']
    
    # Allow the entire supervisor network range for Home Assistant integrations
    if client_ip and (client_ip in allowed_ips or client_ip.startswith('172.30.32.')):
        return
    
    logger.warning(f"Blocked request from unauthorized IP: {client_ip}")
    abort(403)  # Forbidden

@app.route('/')
def index():
    return render_template('index.html', status=monitor.get_status())

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'SFELAPCO Monitor'})

@app.route('/debug')
def debug():
    """Debug route to check ingress headers and connection info"""
    return jsonify({
        'remote_addr': request.environ.get('REMOTE_ADDR'),
        'headers': dict(request.headers),
        'ingress_path': request.headers.get('X-Ingress-Path', 'Not set'),
        'method': request.method,
        'url': request.url,
        'current_charge': monitor.current_charge,
        'last_update': monitor.last_update,
        'update_interval_days': monitor.update_interval_days,
        'retain_history': monitor.retain_history,
        'max_history_days': monitor.max_history_days
    })

@app.route('/api/status')
def api_status():
    try:
        return jsonify(monitor.get_status())
    except Exception as e:
        logger.error(f"Error in status API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')  
def api_history():
    try:
        return jsonify(monitor.get_history())
    except Exception as e:
        logger.error(f"Error in history API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update')
def api_update():
    try:
        logger.info("Manual update requested via web interface")
        success = monitor.scrape_generation_charge()
        result = {'success': success, 'status': monitor.get_status()}
        logger.info(f"Manual update result: {success}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in manual update: {e}")
        return jsonify({'success': False, 'error': str(e), 'status': monitor.get_status()}), 500

def run_scheduler():
    """Run the scheduled tasks"""
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """Main function"""
    logger.info("Starting SFELAPCO Generation Charge Monitor")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    try:
        # Initial data fetch
        logger.info("Performing initial data fetch...")
        success = monitor.scrape_generation_charge()
        if success:
            logger.info("Initial data fetch successful")
        else:
            logger.warning("Initial data fetch failed, will retry on schedule")
        
        # Schedule regular updates
        schedule.every(monitor.update_interval_days).days.do(monitor.scrape_generation_charge)
        logger.info(f"Scheduled updates every {monitor.update_interval_days} days")
        
        # Start scheduler in background thread
        scheduler_thread = Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Scheduler thread started")
        
        # Start Flask web interface
        logger.info("Starting web interface on port 8099")
        logger.info("Access methods:")
        logger.info("  1. Home Assistant Ingress: Use 'OPEN WEB UI' button in addon")
        logger.info("  2. Direct API Access: http://localhost:8099 (for integrations)")
        logger.info("Security: Only accepting connections from Home Assistant supervisor network")
        
        # Start Flask with dual access configuration
        app.run(host='0.0.0.0', port=8099, debug=False, threaded=True, use_reloader=False)
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

if __name__ == '__main__':
    main()
