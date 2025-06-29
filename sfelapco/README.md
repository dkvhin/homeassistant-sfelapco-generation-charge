# SFELAPCO Generation Charge Monitor

A Home Assistant addon that monitors and tracks the monthly generation charges from San Fernando Electric Light And Power Company (SFELAPCO). This addon provides a web interface for viewing current rates and historical data.

## Features

- 🔄 **Automatic Data Fetching**: Regularly scrapes generation charge data from the SFELAPCO website
- 📊 **Historical Tracking**: Maintains a history of generation charges over time
-  **Web Interface**: Beautiful web dashboard to view current rates and history
- ⚙️ **Configurable**: Adjustable update intervals and data retention settings
- 🔌 **API Access**: RESTful API for integration with Home Assistant or other systems

## Installation

1. Add this addon to your Home Assistant Supervisor
2. Configure the addon options (optional)
3. Start the addon
4. Access the web interface via the "OPEN WEB UI" button

## Configuration

```yaml
update_interval: 1.0         # Update interval in days (default: 1 day)
retain_history: true         # Whether to keep historical data
max_history_days: 365        # Maximum days of history to keep
```

### Configuration Options

- **update_interval**: How often to check for new data (0.1-30.0 days)
- **retain_history**: Set to `false` to disable historical data collection
- **max_history_days**: Maximum number of days to keep historical data (1-1095 days)

## API Endpoints

The addon provides several API endpoints for integration:

- `GET /api/status` - Current status and configuration
- `GET /api/history` - Historical charge data
- `POST /api/update` - Manually trigger data update
- `GET /health` - Health check endpoint

### Example API Usage

```bash
# Get current status
curl http://your-ha-instance:8099/api/status

# Get historical data
curl http://your-ha-instance:8099/api/history

# Trigger manual update
curl -X POST http://your-ha-instance:8099/api/update
```

## Home Assistant Integration

For Home Assistant sensor integration, create a separate custom integration or use the RESTful sensor platform:

```yaml
# In your Home Assistant configuration.yaml
sensor:
  - platform: rest
    name: "SFELAPCO Generation Charge"
    resource: "http://localhost:8099/api/status"
    value_template: "{{ value_json.current_charge.rate if value_json.current_charge else 'unavailable' }}"
    unit_of_measurement: "PHP/kWh"
    device_class: monetary
    icon: "mdi:flash"
    scan_interval: 3600  # Update every hour
    json_attributes:
      - current_charge
      - last_update
      - history_count
```

### Example Automations

#### Get notification when rates change
```yaml
automation:
  - alias: "SFELAPCO Rate Change Alert"
    trigger:
      - platform: state
        entity_id: sensor.sfelapco_generation_charge
    condition:
      - condition: template
        value_template: "{{ trigger.from_state.state != trigger.to_state.state }}"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "SFELAPCO generation charge changed to ₱{{ states('sensor.sfelapco_generation_charge') }}/kWh"
```

#### Track monthly electricity costs
```yaml
sensor:
  - platform: template
    sensors:
      monthly_electricity_cost:
        friendly_name: "Estimated Monthly Electricity Cost"
        unit_of_measurement: "PHP"
        value_template: >
          {% set usage = states('sensor.monthly_energy_usage') | float %}
          {% set rate = states('sensor.sfelapco_generation_charge') | float %}
          {{ (usage * rate) | round(2) }}
```

## Web Interface

The addon includes a modern, responsive web interface accessible at:
`http://homeassistant.local:8099`

Features:
- Current generation charge display
- Service statistics
- Manual update button
- Historical data viewer
- Auto-refresh functionality

## Data Source

The addon fetches data from: https://sfelapco.com/content.php?content_id=302

The website displays generation charges in the format:
"Month Year: Php X.XXXXX"

## Troubleshooting

### No data appearing
1. Check the addon logs for error messages
2. Verify internet connectivity
3. Try manually updating via the web interface

### MQTT sensors not showing in Home Assistant
1. Ensure MQTT is configured in Home Assistant
2. Check that the Mosquitto broker addon is running
3. Restart the addon after ensuring MQTT is working

### Web interface not accessible
1. Check if port 8099 is available
2. Restart the addon
3. Check addon logs for Flask startup errors

## Logs

View addon logs through the Home Assistant Supervisor interface to debug issues.

## Support

This addon monitors the SFELAPCO website for generation charge updates. If the website structure changes, the addon may need updates to continue working properly.

## License

This addon is provided as-is for educational and personal use.
