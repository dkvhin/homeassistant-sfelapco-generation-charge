# SFELAPCO Generation Charge Monitor Add-ons

This repository contains Home Assistant add-ons and integrations for monitoring SFELAPCO (San Fernando Electric Light And Power Company) generation charges and electricity rates.

Add-on documentation: <https://developers.home-assistant.io/docs/add-ons>

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fyourusername%2Fhomeassistant-sfelapco-generation-charge)

## Add-ons

This repository contains the following add-ons:

### [SFELAPCO Generation Charge Monitor](./sfelapco)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

_Monitor SFELAPCO monthly generation charges and electricity rates with web interface and API access._

## Home Assistant Integration

This repository also includes a **proper custom Home Assistant integration** for seamless sensor creation:

### [SFELAPCO Custom Integration](./home_assistant_integration)

A fully UI-configurable Home Assistant integration that creates sensors by polling the addon's API. Features:

- **UI Configuration**: No YAML required - fully configurable through Home Assistant's UI
- **Device Registry Support**: Creates a proper device in Home Assistant's device registry
- **Config Flow Setup**: Easy setup via Settings → Integrations with connection testing
- **Data Coordinator**: Efficient API polling with proper error handling
- **Rich Sensor Attributes**: Additional context data for automations and dashboards
- **Automatic Updates**: Polls addon every hour for the latest generation charge data

**Entities Created:**
- `sensor.generation_charge` - Current generation charge rate (PHP/kWh)
- `sensor.last_update` - Timestamp of last successful update

## Installation Options

### Option 1: Addon Only (Web Interface + API)
1. Add this repository to Home Assistant Supervisor
2. Install the SFELAPCO addon
3. Use the web interface at `http://homeassistant.local:8099`
4. Optionally integrate via RESTful sensors (manual YAML configuration)

### Option 2: Addon + Custom Integration (Recommended)
1. Install the addon (as above)
2. Copy the `home_assistant_integration/sfelapco` folder to `<config>/custom_components/sfelapco`
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "SFELAPCO Generation Charge Monitor" and configure

### Why Use the Custom Integration?

- **No YAML Configuration**: Everything is configured through the UI
- **Proper Device Management**: Shows up as a device in Home Assistant with all sensors grouped
- **Better Error Handling**: Automatic retries and clear error reporting
- **Rich Attributes**: More data available for automations and dashboards
- **Maintenance**: Easier to update and manage through the Home Assistant UI

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'sfelapco/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'sfelapco/config.yaml' when you do that.
  - Make sure you update 'sfelapco/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'sfelapco/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Adjust all keys/url's that points to 'yourusername' to now point to your actual user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
