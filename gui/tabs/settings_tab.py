"""
Settings Tab
Application settings and configuration
"""

import customtkinter as ctk
import logging
from core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class SettingsTab:
    """Settings tab component"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        
        # API Settings
        api_frame = ctk.CTkFrame(parent)
        api_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        api_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(api_frame, text="API Configuration", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        ctk.CTkLabel(api_frame, text="API Key:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.api_key_entry = ctk.CTkEntry(api_frame, show="*")
        self.api_key_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        self.api_key_entry.insert(0, self.config.get("api_key", ""))
        
        ctk.CTkLabel(api_frame, text="API Secret:"YOUR_SECRET_HERE"w", padx=10, pady=5)
        self.api_secret_entry = ctk.CTkEntry(api_frame, show="*")
        self.api_secret_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        self.api_secret_entry.insert(0, self.config.get("api_secret", ""))
        
        ctk.CTkLabel(api_frame, text="Roblox Cookie:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.cookie_entry = ctk.CTkEntry(api_frame, show="*")
        self.cookie_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        self.cookie_entry.insert(0, self.config.get("roblox_cookie", ""))
        
        # Appearance Settings
        appearance_frame = ctk.CTkFrame(parent)
        appearance_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        appearance_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(appearance_frame, text="Appearance", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        ctk.CTkLabel(appearance_frame, text="Theme:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.theme_var = ctk.StringVar(value=self.config.get("theme", "dark"))
        theme_menu = ctk.CTkComboBox(
            appearance_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self.change_theme
        )
        theme_menu.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Features Settings
        features_frame = ctk.CTkFrame(parent)
        features_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        features_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(features_frame, text="Features", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.feature_vars = {}
        features = self.config.get("features", {})
        
        row = 1
        for feature_name, enabled in features.items():
            var = ctk.BooleanVar(value=enabled)
            self.feature_vars[feature_name] = var
            checkbox = ctk.CTkCheckBox(
                features_frame,
                text=feature_name.replace("_", " ").title(),
                variable=var
            )
            checkbox.grid(row=row, column=0, sticky="w", padx=20, pady=5)
            row += 1
        
        # Save button
        save_btn = ctk.CTkButton(
            parent,
            text="Save Settings",
            command=self.save_settings,
            fg_color="green"
        )
        save_btn.grid(row=3, column=0, padx=10, pady=10)
    
    def change_theme(self, value):
        """Change application theme"""
        ctk.set_appearance_mode(value)
        self.config["theme"] = value
    
    def save_settings(self):
        """Save all settings"""
        self.config["api_key"] = self.api_key_entry.get()
        self.config["api_secret"] = self.api_secret_entry.get()
        self.config["roblox_cookie"] = self.cookie_entry.get()
        self.config["theme"] = self.theme_var.get()
        
        # Update features
        for feature_name, var in self.feature_vars.items():
            self.config["features"][feature_name] = var.get()
        
        if self.config_manager.save_config(self.config):
            self.main_window.update_status("Settings saved successfully")
            logger.info("Settings saved")

