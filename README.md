# Tapo L530E Color Synchronization

Synchronize your TP-Link Tapo L530E smart bulb with the dominant colors on your monitor! This project provides a Python script that dynamically updates your bulb's color based on your screen, using the official [tapo](https://pypi.org/project/tapo/) Python bindings (which are powered by a Rust backend).

## Features
- Real-time color sync between your monitor and Tapo L530E smart bulb
- Smooth color transitions
- Multi-monitor support
- Easily extensible for other Tapo color bulbs

## Project Structure
- `tapo_screen_sync.py` — Main Python script for color synchronization
- `config.ini` — Configuration file for your Tapo credentials and bulb IP
- `tapo-0.8.1/` — Contains the Rust library and Python bindings for Tapo devices
- `test_monitors.py` — Utility to list your monitors
- `tapo_sync.bat` — Windows batch file to launch the sync script interactively
- `log.txt` — Log file for errors and debug output

## Requirements
- **Python 3.12** or newer
- The following Python libraries:
  ```bash
  pip install tapo mss Pillow numpy opencv-python colorsys
  ```
- A Tapo L530E (or compatible) smart bulb

## Setup
1. **Clone this repository**
2. **Install dependencies** (see above)
3. **Configure your Tapo credentials and device IP:**
   Edit `config.ini`:
   ```ini
   [TapoSettings]
   username=YOUR_EMAIL
   password=YOUR_PASSWORD
   ip_address=YOUR_BULB_IP
   ```
4. **(Optional) List your monitors:**
   ```bash
   python test_monitors.py
   ```
   This will print all available monitors and their indices.

## Usage
### Windows (with batch file)
Double-click `tapo_sync.bat` and follow the prompt to select your monitor.

### Command Line
```bash
python tapo_screen_sync.py [MONITOR_INDEX]
```
- `MONITOR_INDEX` (optional): The index of the monitor to sync (default: 1)

### What the script does
- Connects to your Tapo L530E using the credentials in `config.ini`
- Captures the dominant color from the selected monitor
- Smoothly transitions the bulb to match the screen color in real time

## Troubleshooting
- If you see errors about missing attributes (e.g., `set_light_state`), ensure you have the latest `tapo` Python package installed.
- Check `log.txt` for error messages.
- Make sure your bulb is online and the IP address is correct.

## Advanced: Rust and Python Bindings
This project uses the [tapo](https://crates.io/crates/tapo) Rust library and its Python bindings. You can:
- Explore Rust examples in `tapo-0.8.1/tapo/examples/`
- Explore Python examples in `tapo-0.8.1/tapo-py/examples/`
- Build the Rust library or Python bindings yourself (see `tapo-0.8.1/README.md` for details)

## License
MIT License — see [LICENSE](LICENSE)

## Credits
- [mihai-dinculescu/tapo](https://github.com/mihai-dinculescu/tapo) for the Tapo API library
- Project by Orhan Cenk Akcadoğan
  
