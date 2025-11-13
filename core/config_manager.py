"""
Configuration Manager
Handles loading and saving of user configuration
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = Path("config")
        self.config_file = self.config_dir / "config.json"
        self.template_file = self.config_dir / "config_template.json"
        self.config_dir.mkdir(exist_ok=True)
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._get_default_config()
        else:
            # Create from template if exists
            if self.template_file.exists():
                try:
                    with open(self.template_file, 'r') as f:
                        config = json.load(f)
                    # Save as actual config
                    with open(self.config_file, 'w') as f:
                        json.dump(config, f, indent=4)
                    return config
                except Exception:
                    pass
            return self._get_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "api_key": "YOUR_API_KEY_HERE",
            "api_secret": "YOUR_SECRET_HERE",
            "roblox_cookie": "",
            "auto_start": False,
            "theme": "dark",
            "window_size": {"width": 1200, "height": 800},
            "features": {
                "script_executor": True,
                "auto_farm": True,
                "macro": True,
                "visit_bot": True,
                "server_bot": False
            },
            "game_configs": {}
        }

