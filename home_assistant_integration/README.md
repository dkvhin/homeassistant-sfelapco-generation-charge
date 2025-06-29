# SFELAPCO Home Assistant Custom Integration

This custom integration provides sensor entities for monitoring SFELAPCO generation charges in Home Assistant. It connects to the SFELAPCO addon via its REST API to fetch the latest generation charge information.

## Features

- **UI Configuration**: Fully configurable through Home Assistant's UI (no YAML configuration required)
- **Device Registry Support**: Creates a proper device in Home Assistant's device registry
- **Automatic Updates**: Polls the addon every hour for the latest generation charge data
- **Error Handling**: Robust error handling with connection timeouts and retries
- **Sensor Entities**:
  - `sensor.generation_charge`: Current generation charge rate (PHP/kWh)
  - `sensor.last_update`: Timestamp of the last successful data update

## Prerequisites

Before installing this integration, make sure you have:

1. **SFELAPCO Addon** installed and running in your Home Assistant instance
2. The addon should be accessible at the configured host and port (default: localhost:8099)
3. The addon's REST API should be responding to health checks

## Installation

### Method 1: Manual Installation

1. Copy the entire `sfelapco` folder to your Home Assistant's `custom_components` directory:
   ```
   /config/custom_components/sfelapco/
   ```

2. Restart Home Assistant

3. Go to **Settings** → **Devices & Services** → **Add Integration**

4. Search for "SFELAPCO Generation Charge Monitor" and click on it

5. Enter the addon's connection details:
   - **Host**: Use `localhost` or `127.0.0.1` (the addon exposes port 8099 for direct access)
   - **Port**: Use `8099` (this is the exposed port from the addon configuration)

6. Click **Submit** to complete the setup

### Method 2: HACS (if available)

This integration can be added to HACS as a custom repository:

1. Go to **HACS** → **Integrations** → **Custom Repositories**
2. Add the repository URL: `https://github.com/yourusername/homeassistant-sfelapco-generation-charge`
3. Select **Integration** as the category
4. Install the integration through HACS
5. Restart Home Assistant and configure as described above

## Configuration

The integration is **fully UI-configurable** - no YAML configuration is required or supported.

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| Host | Yes | localhost | Hostname or IP address of the SFELAPCO addon |
| Port | Yes | 8099 | Port number of the SFELAPCO addon |

### Connection Testing

The integration will automatically test the connection during setup by:
1. Making a health check request to `http://{host}:{port}/health`
2. Verifying the addon responds with the correct service identification
3. Displaying appropriate error messages if connection fails

## Entities

Once configured, the integration creates the following entities:

### Generation Charge Sensor
- **Entity ID**: `sensor.generation_charge`
- **Device Class**: Monetary
- **Unit**: PHP/kWh
- **State Class**: Measurement
- **Attributes**:
  - `month`: Current month for the charge
  - `year`: Current year for the charge  
  - `timestamp`: When the charge was set
  - `last_update`: Last successful update from the addon
  - `history_count`: Number of historical records

### Last Update Sensor
- **Entity ID**: `sensor.last_update`
- **Device Class**: Timestamp
- **Attributes**:
  - `update_interval_days`: Addon's update interval
  - `retain_history`: Whether history is retained
  - `max_history_days`: Maximum days of history kept

## Device Registry

The integration creates a device in Home Assistant's device registry with:
- **Name**: SFELAPCO Monitor ({host}:{port})
- **Manufacturer**: SFELAPCO
- **Model**: Generation Charge Monitor
- **Configuration URL**: Link to the addon's web interface

## Requirements

- SFELAPCO Generation Charge Monitor addon must be installed and running
- Home Assistant 2023.1 or later
- Python 3.11+ (handled by Home Assistant)

## Troubleshooting

### Integration Setup Issues

1. **Cannot Connect Error**:
   - Verify the SFELAPCO addon is running and started
   - Check that the addon has port 8099 exposed (should be in addon configuration)
   - Use `localhost` or `127.0.0.1` as the host (not your Home Assistant's external IP)
   - Ensure the port is `8099` (this is the addon's exposed port)
   - Check addon logs for any startup errors
   - Test direct access: try visiting `http://homeassistant.local:8099/health` in a browser

2. **Already Configured Error**:
   - The same host:port combination is already configured
   - Remove the existing configuration and try again
   - Use a different port if running multiple instances

### Runtime Issues

1. **Sensors Show "Unavailable"**:
   - Check if the addon is still running
   - Verify network connectivity
   - Check Home Assistant logs for error messages
   - Restart the integration from the UI

2. **Data Not Updating**:
   - Check the addon's update interval settings
   - Verify the addon is successfully fetching data from SFELAPCO
   - Check both addon and integration logs

### Debug Information

The addon provides debug endpoints that can help with troubleshooting:
- `GET /debug/logs` - Recent log entries
- `GET /debug/config` - Current addon configuration
- `GET /health` - Service health status

## Usage Examples

### Displaying in Lovelace

Add the sensors to your Lovelace dashboard:

```yaml
type: entities
entities:
  - entity: sensor.generation_charge
    name: Current Generation Charge
  - entity: sensor.last_update
    name: Last Updated
```

### Creating Automations

Create automations based on generation charge changes:

```yaml
automation:
  - alias: "Generation Charge Alert"
    trigger:
      - platform: state
        entity_id: sensor.generation_charge
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state | float > 5.0 }}"
    action:
      - service: notify.notify
        data:
          message: "Generation charge is now {{ states('sensor.generation_charge') }} PHP/kWh"
```

## Support

For issues related to:
- **Integration functionality**: Create an issue in this repository
- **Addon functionality**: Check the main SFELAPCO addon documentation
- **Home Assistant setup**: Consult Home Assistant documentation

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
