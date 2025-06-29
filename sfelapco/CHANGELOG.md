# Changelog

All notable changes to the SFELAPCO Generation Charge Monitor addon will be documented in this file.

## [1.0.2] - 2025-06-29

### Breaking Changes
- **REMOVED MQTT integration** - The addon now focuses on data collection and web interface only
- Home Assistant integration moved to separate custom integration (see `/home_assistant_integration`)

### Added
- RESTful API endpoints for integration (`/api/status`, `/api/history`, `/api/update`)
- Enhanced web interface for viewing current rates and history
- Better error handling and logging
- Production WSGI server (Gunicorn) support

### Changed
- Simplified addon configuration (removed MQTT-related options)
- Updated documentation with API usage examples
- Improved performance by removing MQTT dependencies

### Migration Guide
For Home Assistant sensor integration:
1. **Option 1**: Use the new custom integration (recommended)
   - Copy `home_assistant_integration/sfelapco` to `<config>/custom_components/sfelapco`
   - Restart HA and add integration via UI

2. **Option 2**: Use RESTful sensor platform
   ```yaml
   sensor:
     - platform: rest
       name: "SFELAPCO Generation Charge"
       resource: "http://localhost:8099/api/status"
       value_template: "{{ value_json.current_charge.rate if value_json.current_charge else 'unavailable' }}"
       unit_of_measurement: "PHP/kWh"
   ```

## [1.0.0] - 2025-06-29

### Added
- Initial release of SFELAPCO Generation Charge Monitor
- Automatic scraping of generation charges from SFELAPCO website
- Home Assistant MQTT integration with auto-discovery
- Web interface for monitoring and manual updates
- Historical data tracking and retention
- Configurable update intervals
- Responsive web dashboard with modern UI
- Real-time data display and statistics
- Manual update functionality
- Historical data viewer
- Error handling and logging
- Data persistence across addon restarts

### Features
- **Data Sources**: Fetches from https://sfelapco.com/content.php?content_id=302
- **Update Frequency**: Configurable (default: hourly)
- **Data Retention**: Configurable history retention (default: 365 days)
- **Home Assistant Integration**: Automatic sensor creation via MQTT discovery
- **Web Interface**: Accessible on port 8099
- **Sensors Created**:
  - `sensor.sfelapco_generation_charge`: Current rate in PHP/kWh
  - `sensor.sfelapco_last_update`: Last successful update timestamp

### Technical Details
- Built with Python 3
- Uses Flask for web interface
- BeautifulSoup for web scraping
- MQTT for Home Assistant integration
- Scheduled updates with configurable intervals
- JSON data persistence
- Comprehensive error handling and logging
