"""
Roblox Automation Suite - Main Application
A comprehensive automation tool combining features from multiple Roblox tools
Developed by PlayNexus // © 2025 Nortaq
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import customtkinter as ctk
    from gui.main_window import MainWindow
    from core.config_manager import ConfigManager
    from core.logger import setup_logger
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point for the application"""
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Roblox Automation Suite")
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    # Initialize GUI
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = MainWindow(config)
    app.mainloop()

if __name__ == "__main__":
    main()

