# Home Assistant Add-on: SFELAPCO Generation Charge Monitor

## Installation

1. Add this repository to your Home Assistant Supervisor:
   - Navigate to the Supervisor panel in Home Assistant
   - Click on the Add-on Store
   - Click on the three dots menu (⋮) in the top right
   - Select "Repositories"
   - Add this repository URL: `https://github.com/yourusername/homeassistant-sfelapco-generation-charge`
   - Click "Add"

2. Install the SFELAPCO Generation Charge Monitor add-on:
   - Find the add-on in the store
   - Click "Install"

3. Configure the add-on (optional):
   - Click on the add-on
   - Go to the "Configuration" tab
   - Adjust settings as needed

4. Start the add-on:
   - Click "Start"
   - Optionally enable "Start on boot" and "Watchdog"

## How to use

This add-on monitors the SFELAPCO website for generation charge updates and automatically creates Home Assistant sensors via MQTT discovery.

### Features

- 🔄 **Automatic Data Fetching**: Regularly scrapes generation charge data from the SFELAPCO website
- 📊 **Historical Tracking**: Maintains a history of generation charges over time  
-  **Web Interface**: Beautiful web dashboard to view current rates and history
- ⚙️ **Configurable**: Adjustable update intervals and data retention settings
- 🔌 **API Access**: RESTful API for integration with Home Assistant or other systems

### Web Interface

After starting the add-on, you can access the web interface in two ways:

1. **Home Assistant Ingress**: Click "OPEN WEB UI" in the add-on details for a seamless experience
2. **Direct Access**: Visit `http://homeassistant.local:8099` (or use your Home Assistant IP address)

The web interface provides:

- Current generation charge rate
- Historical data visualization
- Update status and logs
- Debug information for troubleshooting

### API Integration

The add-on exposes port 8099 and provides RESTful API endpoints for integration with Home Assistant or other systems:

**Base URL**: `http://localhost:8099` (when accessed from within Home Assistant)

**Available Endpoints**:

- `/api/status` - Get current status and configuration
- `/api/history` - Get historical charge data
- `/api/update` - Manually trigger data update

### Home Assistant Integration

For Home Assistant integration, you can use the RESTful sensor platform to create sensors from the add-on's API:

```yaml
sensor:
  - platform: rest
    name: "SFELAPCO Generation Charge"
    resource: "http://localhost:8099/api/status"
    value_template: "{{ value_json.current_charge.rate if value_json.current_charge else 'unavailable' }}"
    unit_of_measurement: "PHP/kWh"
    device_class: monetary
    icon: "mdi:flash"
    scan_interval: 3600
    json_attributes:
      - current_charge
      - last_update
      - history_count
```

## Configuration

```yaml
update_interval: 1.0         # Update interval in days (default: 1 day)
retain_history: true         # Whether to keep historical data
max_history_days: 365        # Maximum days of history to keep
```

### Network Access

The add-on is configured with both ingress and port exposure:

- **Ingress**: Access via Home Assistant's "OPEN WEB UI" button (seamless integration)
- **Port 8099**: Direct network access for API calls from integrations
- **Security**: Only accepts connections from the Home Assistant supervisor network and localhost

This dual configuration allows:
1. User-friendly web interface access through ingress
2. API access for the custom Home Assistant integration
3. Direct API access for advanced users and external tools

### Option: `update_interval`

How often to check for new data from the SFELAPCO website.

- **Required**: No
- **Default**: `1.0`
- **Type**: Float (0.1-30.0)
- **Description**: Update interval in days. For example:
  - `1.0` = Check once per day
  - `0.5` = Check twice per day  
  - `7.0` = Check once per week

### Option: `retain_history`

Whether to keep historical data for tracking trends over time.

- **Required**: No
- **Default**: `true`
- **Type**: Boolean
- **Description**: Set to `false` to disable historical data collection and only track current rates.

### Option: `max_history_days`

Maximum number of days of historical data to keep.

- **Required**: No
- **Default**: `365`
- **Type**: Integer (1-1095)
- **Description**: Older historical data will be automatically cleaned up to keep storage usage reasonable.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Community Forum](https://community.home-assistant.io/)
- The [Home Assistant Discord Chat Server](https://discord.gg/c5DvZ4e) for general Home Assistant discussions and questions
- Join the [r/homeassistant subreddit](https://reddit.com/r/homeassistant) for discussions and help

## Authors & contributors

This add-on is maintained by [Your Name].

For a full list of all authors and contributors, check [the contributor's page on GitHub][contributors].

## License

MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[contributors]: https://github.com/yourusername/homeassistant-sfelapco-generation-charge/graphs/contributors
