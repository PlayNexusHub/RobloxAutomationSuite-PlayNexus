# Roblox Automation Suite

A comprehensive Windows 10 application that combines and enhances features from multiple Roblox automation tools, providing a unified interface for script execution, game automation, bot management, and macro recording.

## Features

### 🎮 Script Executor
- Load and execute Lua scripts in Roblox
- Syntax highlighting and script editor
- Save and manage script libraries

### 🤖 Game Automation

Supports **50+ Roblox games** with specific automation features for each game:

#### ⚔️ Fighting Games (12 games)
- **Blox Fruits** - Fruit farming, auto-raid, boss farming
- **Da Hood** - Cash farming, auto-duel, auto-rob
- **King Legacy** - Quest farming, auto-awaken
- **Project Slayers** - Demon farming, breathing training
- **Shindo Life** - Quest farming, auto-spin bloodlines
- **Ninja Legends** - Chi farming, auto-evolve pets
- **Your Bizarre Adventure** - Stand farming, auto-prestige
- **A One Piece Game** - Devil fruit farming, auto-raid
- **Grand Piece Online** - Devil fruit farming, auto-quest
- **Slap Battles** - Auto-slap, glove farming
- **Ability Wars** - Auto-fight
- **Super Power Fighting Simulator** - Power farming

#### 🎮 Simulator Games (8 games)
- **Pet Simulator X** - Auto-hatch eggs, coin farming, auto-trade
- **Pet Simulator 99** - Auto-hatch, coin farming
- **Bee Swarm Simulator** - Pollen collection, honey conversion
- **Mining Simulator 2** - Auto-mine ores, auto-sell
- **Adopt Me** - Auto-age pets, auto-trade
- **Clicker Simulator** - Auto-click, auto-rebirth
- **Tapping Legends X** - Auto-tap
- **Grow a Garden** - 21+ features: plant seeds, water plants, harvest crops, auto-fertilize, upgrade garden, sell produce, buy seeds, auto-weed, pest control, auto-compost, auto-irrigate, auto-prune, harvest all, plant all, upgrade tools, complete orders, collect rewards, manage inventory, optimize layout, full auto cycle

#### 🏰 Tower Defense Games (3 games)
- **Anime Adventures** - Wave farming, auto-summon, auto-upgrade
- **All Star Tower Defense** - Wave farming, auto-summon
- **Tower Defense Simulator** - Wave farming

#### 🎢 Tycoon Games (2 games)
- **Restaurant Tycoon 2** - Auto-cook, auto-serve
- **Theme Park Tycoon** - Auto-collect money, upgrade rides

#### 🏃 Obby Games (3 games)
- **Tower of Hell** - Auto-complete tower
- **Speed Run 4** - Auto-run course
- **Evade** - Auto-evade

#### 🔫 FPS Games (2 games)
- **Arsenal** - Auto-aim assist
- **Phantom Forces** - Kill farming

#### 🗺️ Adventure Games (3 games)
- **Jailbreak** - Auto-rob locations, auto-escape
- **Mad City** - Auto-rob
- **Dragon Adventures** - Auto-breed dragons, coin farming

#### 🏠 Life Games (3 games)
- **Welcome to Bloxburg** - Auto-work jobs
- **Brookhaven** - Auto-roleplay
- **MeepCity** - Auto-work

#### 🧟 Survival Games (2 games)
- **Natural Disaster Survival** - Auto-survive disasters
- **Zombie Rush** - Kill zombies, collect coins

#### 👻 Horror Games (3 games)
- **Doors** - Auto-solve puzzles
- **Rainbow Friends** - Auto-escape
- **Piggy** - Auto-escape

#### 🎯 Other Games (7 games)
- **Build A Boat** - Auto-build, coin farming
- **Murder Mystery 2** - Auto-win games
- **Blade Ball** - Auto-block
- **Rogue Lineage** - Mana farming, auto-grind
- **Deepwoken** - Level farming
- **World Zero** - Quest farming
- **Anime Fighting Simulator** - Chi farming, auto-train

**Total: 48 games** with fully implemented automation features!

### Complete Game List (Alphabetical)

1. A One Piece Game
2. Ability Wars
3. Adopt Me
4. All Star Tower Defense
5. Anime Adventures
6. Anime Fighting Simulator
7. Arsenal
8. Bee Swarm Simulator
9. Blade Ball
10. Blox Fruits
11. Brookhaven
12. Build A Boat
13. Clicker Simulator
14. Da Hood
15. Deepwoken
16. Doors
17. Dragon Adventures
18. Evade
19. Grand Piece Online
20. Grow a Garden
21. Jailbreak
22. King Legacy
23. Mad City
24. MeepCity
25. Mining Simulator 2
26. Murder Mystery 2
27. Natural Disaster Survival
28. Ninja Legends
29. Pet Simulator 99
30. Pet Simulator X
31. Phantom Forces
32. Piggy
33. Project Slayers
34. Rainbow Friends
35. Restaurant Tycoon 2
36. Rogue Lineage
37. Shindo Life
38. Slap Battles
39. Speed Run 4
40. Super Power Fighting Simulator
41. Tapping Legends X
42. Theme Park Tycoon
43. Tower Defense Simulator
44. Tower of Hell
45. Welcome to Bloxburg
46. World Zero
47. Your Bizarre Adventure
48. Zombie Rush

All games feature **game-specific automation options** tailored to each game's mechanics. No generic automation - every game has custom features!

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

