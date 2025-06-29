# SFELAPCO Generation Charge Monitor - Home Assistant Integration

This directory contains a custom Home Assistant integration for the SFELAPCO Generation Charge Monitor addon.

## Installation

1. Copy the `sfelapco` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/sfelapco/
   ```

2. Restart Home Assistant

3. Go to Settings → Devices & Services → Add Integration

4. Search for "SFELAPCO" and follow the setup wizard

## Configuration

During setup, you'll need to provide:
- **Host**: The hostname/IP where the SFELAPCO addon is running (usually `localhost`)
- **Port**: The port the addon is listening on (default: `8099`)

## Sensors Created

The integration creates the following sensors:

- `sensor.sfelapco_generation_charge` - Current generation charge rate (PHP/kWh)
- `sensor.sfelapco_last_update` - Timestamp of last successful data update

## Requirements

- SFELAPCO Generation Charge Monitor addon must be installed and running
- Home Assistant 2023.1 or later

## Features

- Automatic discovery and setup via config flow
- Data coordinator for efficient API polling
- Device and entity registry integration
- Rich attributes for additional data context
