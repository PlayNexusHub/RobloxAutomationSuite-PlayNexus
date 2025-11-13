"""
Main Application Window
Modern GUI using CustomTkinter with enhanced styling
"""

import customtkinter as ctk
import logging
from typing import Dict, Any
from gui.tabs.script_executor_tab import ScriptExecutorTab
from gui.tabs.automation_tab import AutomationTab
from gui.tabs.bot_tab import BotTab
from gui.tabs.macro_tab import MacroTab
from gui.tabs.settings_tab import SettingsTab

logger = logging.getLogger(__name__)

class MainWindow(ctk.CTk):
    """Main application window with enhanced UI"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        
        self.config = config
        
        # Enhanced window configuration
        self.title("🌌 Roblox Automation Suite - PlayNexus")
        width = config.get('window_size', {}).get('width', 1400)
        height = config.get('window_size', {}).get('height', 900)
        self.geometry(f"{width}x{height}")
        self.minsize(1000, 700)
        
        # Center window
        self._center_window()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Header frame with branding
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)
        
        # Logo/Branding
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌌 Roblox Automation Suite",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Version label
        version_label = ctk.CTkLabel(
            header_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Main content area
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Create tabview with enhanced styling
        self.tabview = ctk.CTkTabview(
            content_frame,
            corner_radius=10,
            border_width=2,
            border_color=("#3B8ED0", "#1F6AA5")
        )
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        self.tabs = {}
        self._create_tabs()
        
        # Enhanced status bar
        status_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✓ Ready",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        logger.info("Main window initialized with enhanced UI")
    
    def _center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_tabs(self):
        """Create all tabs with icons"""
        # Script Executor Tab
        self.tabs["executor"] = self.tabview.add("📜 Script Executor")
        ScriptExecutorTab(self.tabs["executor"], self)
        
        # Automation Tab
        self.tabs["automation"] = self.tabview.add("🤖 Automation")
        AutomationTab(self.tabs["automation"], self)
        
        # Bot Tab
        self.tabs["bot"] = self.tabview.add("🚀 Bots")
        BotTab(self.tabs["bot"], self)
        
        # Macro Tab
        self.tabs["macro"] = self.tabview.add("⌨️ Macro/Clicker")
        MacroTab(self.tabs["macro"], self)
        
        # Settings Tab
        self.tabs["settings"] = self.tabview.add("⚙️ Settings")
        SettingsTab(self.tabs["settings"], self)
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status bar with color coding"""
        colors = {
            "info": "gray",
            "success": "green",
            "warning": "orange",
            "error": "red"
        }
        icons = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "error": "✗"
        }
        
        color = colors.get(status_type, "gray")
        icon = icons.get(status_type, "ℹ")
        
        self.status_label.configure(
            text=f"{icon} {message}",
            text_color=color
        )
        logger.debug(f"Status ({status_type}): {message}")
