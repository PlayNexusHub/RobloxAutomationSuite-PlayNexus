# Quick Start Guide

## Installation

1. **Install Python 3.8+** (if building from source)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode
```bash
python main.py
```

Or use the batch file:
```bash
run.bat
```

### Building Release

1. **Run sanitization and build:**
   ```bash
   python build/build.py
   ```

2. **Output:**
   - Executable: `dist/RobloxAutomationSuite.exe`
   - Release package: `Final_Build_RobloxAutomationSuite/`
   - ZIP archive: `Final_Build_RobloxAutomationSuite_v1.0.0.zip`

## Configuration

1. Copy `config/config_template.json` to `config/config.json`
2. Edit `config/config.json` with your API keys
3. Or use `.env.example` as template for `.env` file

## Features Overview

### Script Executor
- Load `.lua` files
- Execute scripts in Roblox
- Save/load script libraries

### Automation
- Select game (Blox Fruits, Da Hood, Anime Adventures)
- Configure automation options
- Start/pause/stop automation

### Bots
- Create visit bots, server bots, follow bots
- Manage multiple bots
- View bot statistics

### Macro/Clicker
- Auto-clicker with CPS control
- Record mouse/keyboard macros
- Save and load macro files

### Settings
- Configure API keys securely
- Change theme (dark/light/system)
- Enable/disable features

## Troubleshooting

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### GUI Not Showing
- Verify CustomTkinter is installed: `pip install customtkinter`
- Check for error messages in console

### Build Issues
- Install Nuitka: `pip install nuitka`
- Or use PyInstaller: `pip install pyinstaller`
- Check build logs in `build_logs/`

## Support

- GitHub: https://github.com/PlayNexusHub
- Discord: https://discord.gg/vFX5mFQUmc

