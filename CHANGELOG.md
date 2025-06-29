# Changelog

All notable changes to the SFELAPCO Generation Charge Monitor addon will be documented in this file.

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
