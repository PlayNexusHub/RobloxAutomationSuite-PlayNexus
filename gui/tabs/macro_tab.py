"""
Macro/Clicker Tab
Enhanced interface for macro recording and automated clicking
"""

import customtkinter as ctk
import logging
from tkinter import filedialog
from modules.macro_clicker import MacroClicker, MacroRecorder

logger = logging.getLogger(__name__)

class MacroTab:
    """Enhanced macro/clicker tab component"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.clicker = MacroClicker()
        self.recorder = MacroRecorder()
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Auto Clicker section
        clicker_container = ctk.CTkFrame(parent, corner_radius=10)
        clicker_container.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        clicker_container.grid_columnconfigure(1, weight=1)
        
        clicker_title = ctk.CTkLabel(
            clicker_container,
            text="🖱️ Auto Clicker",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        clicker_title.grid(row=0, column=0, columnspan=4, sticky="ew", padx=15, pady=10)
        
        # CPS control
        ctk.CTkLabel(
            clicker_container,
            text="CPS (Clicks Per Second):",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        self.cps_var = ctk.StringVar(value="10")
        cps_entry = ctk.CTkEntry(
            clicker_container,
            textvariable=self.cps_var,
            width=100,
            font=ctk.CTkFont(size=12)
        )
        cps_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        # Position recording
        record_pos_btn = ctk.CTkButton(
            clicker_container,
            text="📍 Record Position",
            command=self.record_position,
            width=150,
            font=ctk.CTkFont(size=11)
        )
        record_pos_btn.grid(row=1, column=2, padx=5, pady=10)
        
        # Control buttons
        start_click_btn = ctk.CTkButton(
            clicker_container,
            text="▶ Start Clicking",
            command=self.start_clicking,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=130,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        start_click_btn.grid(row=1, column=3, padx=5, pady=10)
        
        stop_click_btn = ctk.CTkButton(
            clicker_container,
            text="⏹ Stop Clicking",
            command=self.stop_clicking,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=130,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        stop_click_btn.grid(row=1, column=4, padx=15, pady=10)
        
        # Macro Recorder section
        macro_container = ctk.CTkFrame(parent, corner_radius=10)
        macro_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        macro_container.grid_columnconfigure(0, weight=1)
        macro_container.grid_rowconfigure(1, weight=1)
        
        macro_title = ctk.CTkLabel(
            macro_container,
            text="⌨️ Macro Recorder",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        macro_title.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        # Macro controls
        macro_controls = ctk.CTkFrame(macro_container, fg_color="transparent")
        macro_controls.grid(row=1, column=0, sticky="n", padx=15, pady=10)
        
        start_record_btn = ctk.CTkButton(
            macro_controls,
            text="🔴 Start Recording",
            command=self.start_recording,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=150,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        start_record_btn.pack(side="left", padx=5)
        
        stop_record_btn = ctk.CTkButton(
            macro_controls,
            text="⏹ Stop Recording",
            command=self.stop_recording,
            fg_color="#F39C12",
            hover_color="#E67E22",
            width=150,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        stop_record_btn.pack(side="left", padx=5)
        
        play_macro_btn = ctk.CTkButton(
            macro_controls,
            text="▶ Play Macro",
            command=self.play_macro,
            fg_color="#3498DB",
            hover_color="#2980B9",
            width=150,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        play_macro_btn.pack(side="left", padx=5)
        
        save_macro_btn = ctk.CTkButton(
            macro_controls,
            text="💾 Save Macro",
            command=self.save_macro,
            width=130,
            font=ctk.CTkFont(size=11)
        )
        save_macro_btn.pack(side="left", padx=5)
        
        load_macro_btn = ctk.CTkButton(
            macro_controls,
            text="📂 Load Macro",
            command=self.load_macro,
            width=130,
            font=ctk.CTkFont(size=11)
        )
        load_macro_btn.pack(side="left", padx=5)
        
        # Macro info
        self.macro_info = ctk.CTkLabel(
            macro_container,
            text="No macro recorded",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.macro_info.grid(row=2, column=0, padx=15, pady=10)
        
        # Enhanced status
        status_frame = ctk.CTkFrame(parent, corner_radius=10)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✓ Ready",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
    
    def record_position(self):
        """Record current mouse position"""
        pos = self.clicker.record_click_position()
        self.status_label.configure(
            text=f"📍 Recorded position: {pos}",
            text_color="green"
        )
        self.main_window.update_status(f"Position recorded: {pos}", "success")
    
    def start_clicking(self):
        """Start auto-clicking"""
        try:
            cps = float(self.cps_var.get())
            if cps <= 0 or cps > 100:
                self.status_label.configure(
                    text="⚠ CPS must be between 1 and 100",
                    text_color="orange"
                )
                return
            
            config = {
                "position": "current",
                "clicks_per_second": cps
            }
            if self.clicker.start_clicking(config):
                self.status_label.configure(
                    text=f"▶ Clicking at {cps} CPS",
                    text_color="green"
                )
                self.main_window.update_status(f"Auto-clicker running at {cps} CPS", "success")
        except ValueError:
            self.status_label.configure(
                text="✗ Invalid CPS value",
                text_color="red"
            )
            self.main_window.update_status("Invalid CPS value", "error")
    
    def stop_clicking(self):
        """Stop auto-clicking"""
        if self.clicker.stop_clicking():
            self.status_label.configure(
                text="⏹ Clicking stopped",
                text_color="orange"
            )
            self.main_window.update_status("Auto-clicker stopped", "info")
    
    def start_recording(self):
        """Start macro recording"""
        self.recorder.start_recording()
        self.status_label.configure(
            text="🔴 Recording macro... Press keys and move mouse",
            text_color="red"
        )
        self.macro_info.configure(text="Recording in progress...")
        self.main_window.update_status("Macro recording started", "info")
    
    def stop_recording(self):
        """Stop macro recording"""
        self.recorder.stop_recording()
        action_count = len(self.recorder.macro_actions)
        self.status_label.configure(
            text=f"⏹ Stopped recording. {action_count} actions recorded",
            text_color="orange"
        )
        self.macro_info.configure(
            text=f"Recorded {action_count} actions",
            text_color="green"
        )
        self.main_window.update_status(f"Macro recording stopped: {action_count} actions", "success")
    
    def play_macro(self):
        """Play recorded macro"""
        if not self.recorder.macro_actions:
            self.status_label.configure(
                text="⚠ No macro to play",
                text_color="orange"
            )
            return
        
        if self.recorder.play_macro():
            self.status_label.configure(
                text="✓ Macro playback completed",
                text_color="green"
            )
            self.main_window.update_status("Macro playback completed", "success")
        else:
            self.status_label.configure(
                text="✗ Macro playback failed",
                text_color="red"
            )
    
    def save_macro(self):
        """Save macro to file"""
        if not self.recorder.macro_actions:
            self.status_label.configure(
                text="⚠ No macro to save",
                text_color="orange"
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Macro",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            if self.recorder.save_macro(file_path):
                self.status_label.configure(
                    text=f"✓ Macro saved to {file_path}",
                    text_color="green"
                )
                self.main_window.update_status(f"Macro saved: {file_path}", "success")
    
    def load_macro(self):
        """Load macro from file"""
        file_path = filedialog.askopenfilename(
            title="Load Macro",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            if self.recorder.load_macro(file_path):
                action_count = len(self.recorder.macro_actions)
                self.status_label.configure(
                    text=f"✓ Macro loaded: {action_count} actions",
                    text_color="green"
                )
                self.macro_info.configure(
                    text=f"Loaded {action_count} actions from file",
                    text_color="green"
                )
                self.main_window.update_status(f"Macro loaded: {action_count} actions", "success")
