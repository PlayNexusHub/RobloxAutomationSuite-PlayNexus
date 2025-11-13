# Roblox Automation Suite

A comprehensive Windows 10 application that combines and enhances features from multiple Roblox automation tools, providing a unified interface for script execution, game automation, bot management, and macro recording.

## Features

### 🎮 Script Executor
- Load and execute Lua scripts in Roblox
- Syntax highlighting and script editor
- Save and manage script libraries

### 🤖 Game Automation
- **Blox Fruits**: Auto-farm fruits, auto-raid functionality
- **Da Hood**: Cash farming, auto-duel
- **Anime Adventures**: Wave farming, auto-summon
- Generic automation support for any Roblox game

### 🚀 Bot Framework
- **Visit Bot**: Automatically visit games
- **Server Bot**: Join specific servers
- **Follow Bot**: Follow users
- **Farm Bot**: Automated farming bots
- Manage multiple bots simultaneously

### ⌨️ Macro & Clicker
- Record and playback macros
- Auto-clicker with customizable CPS (clicks per second)
- Position recording for precise clicking
- Save and load macro files

### ⚙️ Settings & Configuration
- Secure API key management
- Customizable themes (dark/light/system)
- Feature toggles
- Persistent configuration

## Installation

1. Download the latest release from [GitHub Releases](https://github.com/PlayNexusHub/RobloxAutomationSuite-PlayNexus/releases)
2. Extract the ZIP file
3. Follow the setup instructions in `SETUP_INSTRUCTIONS.txt`
4. Configure your API keys in the Settings tab
5. Run `RobloxAutomationSuite.exe`

## Configuration

### Initial Setup

1. Open `config_template.json` or `.env.example`
2. Replace placeholders with your actual credentials:
   - `YOUR_API_KEY_HERE` → Your API key
   - `YOUR_SECRET_HERE` → Your API secret
   - `YOUR_ROBLOX_COOKIE_HERE` → Your Roblox authentication cookie
3. Save as `config.json` or `.env`

### Settings Tab

Navigate to the Settings tab in the application to:
- Configure API keys and secrets
- Set your Roblox cookie
- Customize appearance theme
- Enable/disable features

## Usage

### Script Executor
1. Navigate to the "Script Executor" tab
2. Load a Lua script file or paste script content
3. Click "Execute" to run the script
4. Use "Stop" to halt execution

### Game Automation
1. Go to the "Automation" tab
2. Select your game from the dropdown
3. Configure automation options
4. Click "Start" to begin automation
5. Use "Pause" or "Stop" as needed

### Bot Management
1. Open the "Bots" tab
2. Select bot type (Visit Bot, Server Bot, etc.)
3. Enter Game ID
4. Click "Create Bot" to start
5. Manage bots from the list

### Macro/Clicker
1. Navigate to "Macro/Clicker" tab
2. For auto-clicker: Set CPS and click "Start Clicking"
3. For macros: Click "Start Recording", perform actions, then "Stop Recording"
4. Use "Play Macro" to replay recorded actions

## Requirements

- Windows 10 or later
- Roblox installed
- Internet connection for API features

## Security

- **Never share your API keys or cookies publicly**
- All credentials are stored locally in configuration files
- Use at your own risk
- For educational and research purposes only

## Development

### Building from Source

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Building Release

Run the build script:
```bash
python build/build.py
```

This will:
- Sanitize the codebase
- Build standalone executable
- Create release package
- Generate ZIP archive

## Project Structure

```
RobloxAutomationSuite/
├── main.py                 # Main application entry point
├── core/                   # Core modules
│   ├── config_manager.py   # Configuration management
│   ├── logger.py           # Logging utility
│   ├── script_executor.py  # Script execution engine
│   ├── automation_engine.py # Automation core
│   └── bot_framework.py    # Bot management
├── modules/                 # Feature modules
│   ├── game_automation.py  # Game-specific automation
│   └── macro_clicker.py    # Macro and clicker
├── gui/                    # GUI components
│   ├── main_window.py      # Main window
│   └── tabs/               # Tab components
├── config/                 # Configuration files
├── build/                  # Build scripts
└── logs/                   # Application logs
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- All features are tested
- Documentation is updated
- No sensitive data is committed

## License

This project is for educational and research purposes only.

## Support

- **GitHub**: https://github.com/PlayNexusHub
- **Discord**: https://discord.gg/vFX5mFQUmc

## Credits

Developed by **PlayNexus** // © 2025 **Nortaq**

This application incorporates and redesigns features inspired by various open-source Roblox automation tools. All code has been rewritten and redesigned from scratch.

## Disclaimer

⚠️ **For educational and research purposes only.** Use responsibly and in accordance with Roblox's Terms of Service. The developers are not responsible for any misuse of this software.

