"""
Bot Tab
Enhanced interface for managing bots
"""

import customtkinter as ctk
import logging
from core.bot_framework import BotFramework, BotType

logger = logging.getLogger(__name__)

class BotTab:
    """Enhanced bot management tab component"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.bot_framework = BotFramework()
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        # Enhanced create bot section
        create_frame = ctk.CTkFrame(parent, corner_radius=10)
        create_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        create_frame.grid_columnconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            create_frame,
            text="🤖 Create New Bot",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, columnspan=4, sticky="ew", padx=15, pady=10)
        
        # Bot type selection
        ctk.CTkLabel(
            create_frame,
            text="Bot Type:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.bot_type_var = ctk.StringVar(value="Visit Bot")
        bot_type_menu = ctk.CTkComboBox(
            create_frame,
            values=["Visit Bot", "Server Bot", "Follow Bot", "Farm Bot"],
            variable=self.bot_type_var,
            width=150,
            font=ctk.CTkFont(size=11)
        )
        bot_type_menu.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        # Game ID entry
        ctk.CTkLabel(
            create_frame,
            text="Game ID:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        self.game_id_entry = ctk.CTkEntry(
            create_frame,
            width=200,
            placeholder_text="Enter Roblox Game ID",
            font=ctk.CTkFont(size=11)
        )
        self.game_id_entry.grid(row=1, column=3, padx=5, pady=10, sticky="ew")
        
        # Create button
        create_btn = ctk.CTkButton(
            create_frame,
            text="➕ Create Bot",
            command=self.create_bot,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=120,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        create_btn.grid(row=1, column=4, padx=15, pady=10, sticky="e")
        
        # Bots list container
        list_container = ctk.CTkFrame(parent, corner_radius=10)
        list_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(0, weight=1)
        
        # List title
        list_title = ctk.CTkLabel(
            list_container,
            text="📋 Active Bots",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        list_title.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        # Scrollable bots list
        self.bots_listbox = ctk.CTkScrollableFrame(list_container, corner_radius=5)
        self.bots_listbox.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        list_container.grid_rowconfigure(1, weight=1)
        
        # Enhanced stats frame
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure(0, weight=1)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="📊 Total Bots: 0 | Active: 0 | Inactive: 0",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.stats_label.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        self._update_bots_list()
        self._update_stats()
    
    def create_bot(self):
        """Create a new bot"""
        bot_type_str = self.bot_type_var.get()
        game_id = self.game_id_entry.get()
        
        if not game_id:
            self.main_window.update_status("⚠ Please enter a Game ID", "warning")
            return
        
        if not game_id.isdigit():
            self.main_window.update_status("⚠ Game ID must be a number", "warning")
            return
        
        # Map string to BotType
        bot_type_map = {
            "Visit Bot": BotType.VISIT_BOT,
            "Server Bot": BotType.SERVER_BOT,
            "Follow Bot": BotType.FOLLOW_BOT,
            "Farm Bot": BotType.FARM_BOT
        }
        
        bot_type = bot_type_map.get(bot_type_str, BotType.VISIT_BOT)
        bot_id = f"bot_{len(self.bot_framework.bots) + 1}"
        
        config = {
            "game_id": game_id,
            "delay": 5
        }
        
        self.bot_framework.create_bot(bot_id, bot_type, config)
        self.bot_framework.start_bot(bot_id)
        
        self.game_id_entry.delete(0, "end")
        self._update_bots_list()
        self.main_window.update_status(f"✓ Created and started {bot_id}", "success")
    
    def _update_bots_list(self):
        """Update bots list display with enhanced UI"""
        # Clear existing
        for widget in self.bots_listbox.winfo_children():
            widget.destroy()
        
        bots = self.bot_framework.get_all_bots()
        
        if not bots:
            # Empty state
            empty_label = ctk.CTkLabel(
                self.bots_listbox,
                text="No bots created yet. Create one above!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Add bots with enhanced cards
            for bot in bots:
                bot_card = ctk.CTkFrame(self.bots_listbox, corner_radius=8)
                bot_card.pack(fill="x", padx=5, pady=8)
                bot_card.grid_columnconfigure(1, weight=1)
                
                # Bot icon/status indicator
                status_icon = "🟢" if bot.is_active else "⚫"
                icon_label = ctk.CTkLabel(
                    bot_card,
                    text=status_icon,
                    font=ctk.CTkFont(size=20)
                )
                icon_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
                
                # Bot info
                info_frame = ctk.CTkFrame(bot_card, fg_color="transparent")
                info_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
                info_frame.grid_columnconfigure(0, weight=1)
                
                bot_name_label = ctk.CTkLabel(
                    info_frame,
                    text=f"{bot.bot_id}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w"
                )
                bot_name_label.grid(row=0, column=0, sticky="ew")
                
                bot_type_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Type: {bot.bot_type.value.replace('_', ' ').title()}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray",
                    anchor="w"
                )
                bot_type_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))
                
                status_text = "🟢 Active" if bot.is_active else "⚫ Inactive"
                status_color = "green" if bot.is_active else "gray"
                status_label = ctk.CTkLabel(
                    info_frame,
                    text=status_text,
                    font=ctk.CTkFont(size=11),
                    text_color=status_color,
                    anchor="w"
                )
                status_label.grid(row=2, column=0, sticky="ew", pady=(2, 0))
                
                # Action buttons
                button_frame = ctk.CTkFrame(bot_card, fg_color="transparent")
                button_frame.grid(row=0, column=2, padx=10, pady=10)
                
                if bot.is_active:
                    stop_btn = ctk.CTkButton(
                        button_frame,
                        text="⏹ Stop",
                        command=lambda b=bot: self.stop_bot(b.bot_id),
                        fg_color="#E74C3C",
                        hover_color="#C0392B",
                        width=80,
                        font=ctk.CTkFont(size=10)
                    )
                    stop_btn.pack(side="left", padx=3)
                else:
                    start_btn = ctk.CTkButton(
                        button_frame,
                        text="▶ Start",
                        command=lambda b=bot: self.start_bot(b.bot_id),
                        fg_color="#2ECC71",
                        hover_color="#27AE60",
                        width=80,
                        font=ctk.CTkFont(size=10)
                    )
                    start_btn.pack(side="left", padx=3)
                
                remove_btn = ctk.CTkButton(
                    button_frame,
                    text="🗑 Remove",
                    command=lambda b=bot: self.remove_bot(b.bot_id),
                    fg_color="#F39C12",
                    hover_color="#E67E22",
                    width=80,
                    font=ctk.CTkFont(size=10)
                )
                remove_btn.pack(side="left", padx=3)
        
        # Schedule next update
        self.parent.after(2000, self._update_bots_list)
    
    def start_bot(self, bot_id: str):
        """Start a bot"""
        self.bot_framework.start_bot(bot_id)
        self.main_window.update_status(f"✓ Started {bot_id}", "success")
    
    def stop_bot(self, bot_id: str):
        """Stop a bot"""
        self.bot_framework.stop_bot(bot_id)
        self.main_window.update_status(f"⏹ Stopped {bot_id}", "info")
    
    def remove_bot(self, bot_id: str):
        """Remove a bot"""
        self.bot_framework.remove_bot(bot_id)
        self._update_bots_list()
        self.main_window.update_status(f"🗑 Removed {bot_id}", "info")
    
    def _update_stats(self):
        """Update statistics"""
        total_bots = len(self.bot_framework.bots)
        active_bots = sum(1 for bot in self.bot_framework.bots.values() if bot.is_active)
        inactive_bots = total_bots - active_bots
        
        self.stats_label.configure(
            text=f"📊 Total Bots: {total_bots} | 🟢 Active: {active_bots} | ⚫ Inactive: {inactive_bots}"
        )
        self.parent.after(1000, self._update_stats)
