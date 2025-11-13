"""
Script Executor Tab
Enhanced interface for executing Lua scripts
"""

import customtkinter as ctk
import logging
from tkinter import filedialog
from core.script_executor import ScriptExecutor

logger = logging.getLogger(__name__)

class ScriptExecutorTab:
    """Enhanced script executor tab component"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.executor = ScriptExecutor()
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Enhanced toolbar
        toolbar = ctk.CTkFrame(parent, corner_radius=10)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        toolbar.grid_columnconfigure(4, weight=1)
        
        # Toolbar buttons with icons
        load_btn = ctk.CTkButton(
            toolbar,
            text="📂 Load Script",
            command=self.load_script,
            width=120,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        load_btn.grid(row=0, column=0, padx=5, pady=10)
        
        save_btn = ctk.CTkButton(
            toolbar,
            text="💾 Save Script",
            command=self.save_script,
            width=120,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        save_btn.grid(row=0, column=1, padx=5, pady=10)
        
        execute_btn = ctk.CTkButton(
            toolbar,
            text="▶ Execute",
            command=self.execute_script,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=120,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        execute_btn.grid(row=0, column=2, padx=5, pady=10)
        
        stop_btn = ctk.CTkButton(
            toolbar,
            text="⏹ Stop",
            command=self.stop_script,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=120,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        stop_btn.grid(row=0, column=3, padx=5, pady=10)
        
        # Script info
        self.script_info = ctk.CTkLabel(
            toolbar,
            text="Lines: 0 | Characters: 0",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="e"
        )
        self.script_info.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        
        # Enhanced script editor frame
        editor_container = ctk.CTkFrame(parent, corner_radius=10)
        editor_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        editor_container.grid_columnconfigure(0, weight=1)
        editor_container.grid_rowconfigure(0, weight=1)
        
        # Editor title
        editor_title = ctk.CTkLabel(
            editor_container,
            text="📜 Lua Script Editor",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        editor_title.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        # Script editor with better font
        self.script_text = ctk.CTkTextbox(
            editor_container,
            font=("Consolas", 13),
            corner_radius=5,
            border_width=2,
            border_color=("#3B8ED0", "#1F6AA5")
        )
        self.script_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        editor_container.grid_rowconfigure(1, weight=1)
        
        # Bind text change event to update info
        self.script_text.bind("<KeyRelease>", self._update_script_info)
        self.script_text.bind("<Button-1>", self._update_script_info)
        
        # Enhanced status bar
        status_frame = ctk.CTkFrame(parent, corner_radius=10)
        status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✓ Ready to execute scripts",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        self._update_script_info()
    
    def _update_script_info(self, event=None):
        """Update script statistics"""
        content = self.script_text.get("1.0", "end-1c")
        lines = len(content.split('\n'))
        chars = len(content)
        self.script_info.configure(text=f"Lines: {lines} | Characters: {chars}")
    
    def load_script(self):
        """Load script from file"""
        file_path = filedialog.askopenfilename(
            title="Load Script",
            filetypes=[("Lua files", "*.lua"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            content = self.executor.load_script_file(file_path)
            if content:
                self.script_text.delete("1.0", "end")
                self.script_text.insert("1.0", content)
                self.status_label.configure(
                    text=f"✓ Loaded: {file_path}",
                    text_color="green"
                )
                self.main_window.update_status(f"Script loaded: {file_path}", "success")
                self._update_script_info()
    
    def save_script(self):
        """Save script to file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Script",
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            content = self.script_text.get("1.0", "end-1c")
            if self.executor.save_script(content, file_path):
                self.status_label.configure(
                    text=f"✓ Saved: {file_path}",
                    text_color="green"
                )
                self.main_window.update_status(f"Script saved: {file_path}", "success")
    
    def execute_script(self):
        """Execute current script"""
        content = self.script_text.get("1.0", "end-1c")
        if content.strip():
            if self.executor.execute_script(content):
                self.status_label.configure(
                    text="▶ Script executing...",
                    text_color="green"
                )
                self.main_window.update_status("Script executor running", "success")
            else:
                self.status_label.configure(
                    text="✗ Failed to execute script",
                    text_color="red"
                )
                self.main_window.update_status("Script execution failed", "error")
        else:
            self.status_label.configure(
                text="⚠ No script to execute",
                text_color="orange"
            )
            self.main_window.update_status("No script content", "warning")
    
    def stop_script(self):
        """Stop script execution"""
        if self.executor.stop_execution():
            self.status_label.configure(
                text="⏹ Script stopped",
                text_color="orange"
            )
            self.main_window.update_status("Script executor stopped", "info")
