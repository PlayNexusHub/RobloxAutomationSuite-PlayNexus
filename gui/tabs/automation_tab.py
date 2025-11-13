"""
Automation Tab
Enhanced interface for game automation with search and categories
"""

import customtkinter as ctk
import logging
from modules.game_automation import GameAutomationManager
from core.automation_engine import AutomationState

logger = logging.getLogger(__name__)

class AutomationTab:
    """Enhanced automation tab component"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.game_manager = GameAutomationManager()
        self.current_automation = None
        self.config_vars = {}
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        # Top control panel
        top_panel = ctk.CTkFrame(parent, corner_radius=10)
        top_panel.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top_panel.grid_columnconfigure(1, weight=1)
        
        # Search and filter section
        search_frame = ctk.CTkFrame(top_panel)
        search_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_frame, text="🔍 Search:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self._on_search_change())
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search games...",
            font=ctk.CTkFont(size=12)
        )
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Category filter
        ctk.CTkLabel(search_frame, text="📁 Category:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.category_var = ctk.StringVar(value="All")
        categories = ["All"] + self.game_manager.get_categories()
        category_menu = ctk.CTkComboBox(
            search_frame,
            values=categories,
            variable=self.category_var,
            command=self._on_category_change,
            width=150
        )
        category_menu.grid(row=0, column=3, padx=5, pady=5)
        
        # Game selection section
        game_selection_frame = ctk.CTkFrame(top_panel)
        game_selection_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        game_selection_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            game_selection_frame,
            text="🎮 Game:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.game_var = ctk.StringVar(value="Blox Fruits")
        self._update_game_list()
        self.game_menu = ctk.CTkComboBox(
            game_selection_frame,
            values=self.filtered_games,
            variable=self.game_var,
            command=self.on_game_change,
            width=300,
            font=ctk.CTkFont(size=12)
        )
        self.game_menu.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Control buttons with icons
        control_frame = ctk.CTkFrame(top_panel)
        control_frame.grid(row=1, column=3, sticky="e", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶ Start",
            command=self.start_automation,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=100,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(
            control_frame,
            text="⏸ Pause",
            command=self.pause_automation,
            fg_color="#F39C12",
            hover_color="#E67E22",
            width=100,
            state="disabled",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.pause_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹ Stop",
            command=self.stop_automation,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100,
            state="disabled",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # Options container with scrollable frame
        options_container = ctk.CTkFrame(parent, corner_radius=10)
        options_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        options_container.grid_columnconfigure(0, weight=1)
        options_container.grid_rowconfigure(0, weight=1)
        
        # Title for options
        options_title = ctk.CTkLabel(
            options_container,
            text="⚙️ Automation Options",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        options_title.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        self.options_scroll = ctk.CTkScrollableFrame(options_container, corner_radius=5)
        self.options_scroll.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        options_container.grid_rowconfigure(1, weight=1)
        
        # Stats and progress frame
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure(1, weight=1)
        
        # Progress bar
        self.progress_label = ctk.CTkLabel(
            stats_frame,
            text="Status: Idle",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.progress_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(stats_frame, width=300)
        self.progress_bar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.progress_bar.set(0)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Runtime: 0s | Actions: 0 | Errors: 0",
            font=ctk.CTkFont(size=11),
            anchor="e"
        )
        self.stats_label.grid(row=0, column=2, padx=15, pady=10, sticky="e")
        
        self._create_game_options()
        self._update_stats()
    
    def _update_game_list(self):
        """Update filtered game list based on search and category"""
        search_query = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        category = self.category_var.get() if hasattr(self, 'category_var') else "All"
        
        if category == "All":
            games = self.game_manager.list_games()
        else:
            games = self.game_manager.get_games_by_category(category)
        
        if search_query:
            games = [g for g in games if search_query in g.lower()]
        
        self.filtered_games = sorted(games)
        
        if hasattr(self, 'game_menu'):
            self.game_menu.configure(values=self.filtered_games)
            if self.filtered_games and self.game_var.get() not in self.filtered_games:
                self.game_var.set(self.filtered_games[0])
    
    def _on_search_change(self):
        """Handle search text change"""
        self._update_game_list()
    
    def _on_category_change(self, value):
        """Handle category change"""
        self._update_game_list()
    
    def _create_game_options(self):
        """Create options for current game with enhanced UI - ALL GAMES"""
        # Clear existing options
        for widget in self.options_scroll.winfo_children():
            widget.destroy()
        
        self.config_vars = {}
        game_name = self.game_var.get()
        automation = self.game_manager.get_automation(game_name)
        
        # Game info header
        info_frame = ctk.CTkFrame(self.options_scroll, corner_radius=5)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text=f"📋 {game_name} - {automation.category}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=15, pady=10)
        
        # Create game-specific options for ALL games
        row = 0
        
        # ========== FIGHTING GAMES ==========
        if game_name == "Blox Fruits":
            self._create_option_row("Fruit Type:", "fruit", ["Any"] + automation.fruits, row)
            row += 1
            self._create_option_row("Location:", "location", automation.farming_locations, row)
            row += 1
            self._create_option_row("Raid Type:", "raid", ["Normal", "Elite", "Legendary"], row)
            row += 1
            self._create_button_row("▶ Start Fruit Farming", lambda: self._start_blox_fruits(), row)
            row += 1
            self._create_button_row("⚔ Auto Raid", lambda: automation.auto_raid(self.config_vars.get("raid", ctk.StringVar(value="Normal")).get()), row)
            row += 1
            self._create_button_row("👑 Boss Farm", lambda: automation.auto_boss_farm("Raid Boss"), row)
        
        elif game_name == "Da Hood":
            self._create_option_row("Automation Type:", "type", ["Cash Farm", "Auto Duel", "Auto Rob"], row)
            row += 1
            self._create_option_row("Rob Location:", "rob_loc", ["Bank", "Gas Station", "Jewelry Store"], row)
            row += 1
            self._create_button_row("▶ Start Automation", lambda: self._start_da_hood(), row)
        
        elif game_name == "King Legacy":
            self._create_option_row("Quest Type:", "quest", ["Bandit", "Marine", "Boss", "Raid"], row)
            row += 1
            self._create_option_row("Sea:", "sea", ["First Sea", "Second Sea", "Third Sea"], row)
            row += 1
            self._create_button_row("⚔ Farm Quests", lambda: automation.farm_quests(self.config_vars.get("quest", ctk.StringVar(value="Bandit")).get()), row)
            row += 1
            self._create_button_row("✨ Auto Awaken", lambda: automation.auto_awaken(), row)
        
        elif game_name == "Project Slayers":
            self._create_option_row("Demon Type:", "demon", ["Lower Moon", "Upper Moon", "Muzan"], row)
            row += 1
            self._create_option_row("Breathing Style:", "breath", ["Water", "Thunder", "Flame", "Wind"], row)
            row += 1
            self._create_button_row("👹 Farm Demons", lambda: automation.farm_demons(self.config_vars.get("demon", ctk.StringVar(value="Lower Moon")).get()), row)
            row += 1
            self._create_button_row("💨 Auto Train Breathing", lambda: automation.auto_breath(), row)
        
        elif game_name == "Shindo Life":
            self._create_option_row("Quest Type:", "quest", ["Daily", "Weekly", "Boss"], row)
            row += 1
            self._create_button_row("⚔ Farm Quests", lambda: automation.farm_quests(), row)
            row += 1
            self._create_button_row("🎰 Auto Spin Bloodlines", lambda: automation.auto_spin(), row)
        
        elif game_name == "Ninja Legends":
            self._create_option_row("Chi Type:", "chi", ["Normal", "Golden", "Rainbow"], row)
            row += 1
            self._create_button_row("⚡ Farm Chi", lambda: automation.farm_chi(), row)
            row += 1
            self._create_button_row("✨ Auto Evolve Pets", lambda: automation.auto_evolve(), row)
        
        elif game_name == "Super Power Fighting Simulator":
            self._create_option_row("Power Type:", "power", ["Basic", "Advanced", "Legendary"], row)
            row += 1
            self._create_button_row("💪 Farm Powers", lambda: automation.farm_powers(), row)
        
        elif game_name == "Your Bizarre Adventure":
            self._create_option_row("Stand Type:", "stand", ["Common", "Uncommon", "Rare", "Epic", "Legendary"], row)
            row += 1
            self._create_button_row("⭐ Farm Stands", lambda: automation.farm_stands(), row)
            row += 1
            self._create_button_row("⬆ Auto Prestige", lambda: automation.auto_prestige(), row)
        
        elif game_name == "A One Piece Game":
            self._create_option_row("Fruit Type:", "fruit", ["Paramecia", "Zoan", "Logia"], row)
            row += 1
            self._create_button_row("🍎 Farm Devil Fruits", lambda: automation.farm_fruits(), row)
            row += 1
            self._create_button_row("⚔ Auto Raid", lambda: automation.auto_raid(), row)
        
        elif game_name == "Grand Piece Online":
            self._create_option_row("Fruit Type:", "fruit", ["Common", "Uncommon", "Rare", "Legendary"], row)
            row += 1
            self._create_button_row("🍎 Farm Devil Fruits", lambda: automation.farm_fruits(), row)
            row += 1
            self._create_button_row("📜 Auto Quest", lambda: automation.auto_quest(), row)
        
        elif game_name == "Slap Battles":
            self._create_option_row("Glove Type:", "glove", ["Default", "Golden", "Custom"], row)
            row += 1
            self._create_button_row("👋 Auto Slap", lambda: automation.auto_slap(), row)
            row += 1
            self._create_button_row("🧤 Farm Gloves", lambda: automation.farm_gloves(), row)
        
        elif game_name == "Ability Wars":
            self._create_option_row("Ability Type:", "ability", ["Common", "Rare", "Epic", "Legendary"], row)
            row += 1
            self._create_button_row("⚔ Auto Fight", lambda: automation.auto_fight(), row)
        
        # ========== SIMULATOR GAMES ==========
        elif game_name == "Pet Simulator X":
            self._create_option_row("Egg Type:", "egg", ["Basic", "Golden", "Rainbow", "Dark Matter"], row)
            row += 1
            self._create_option_row("World:", "world", ["Spawn", "Forest", "Desert", "Volcano", "Tech World"], row)
            row += 1
            self._create_button_row("🥚 Auto Hatch Eggs", lambda: automation.auto_hatch(self.config_vars.get("egg", ctk.StringVar(value="Basic")).get()), row)
            row += 1
            self._create_button_row("💰 Farm Coins", lambda: automation.auto_farm_coins(self.config_vars.get("world", ctk.StringVar(value="Spawn")).get()), row)
            row += 1
            self._create_button_row("🔄 Auto Trade", lambda: automation.auto_trade(), row)
        
        elif game_name == "Pet Simulator 99":
            self._create_option_row("Egg Type:", "egg", ["Starter", "Golden", "Rainbow"], row)
            row += 1
            self._create_button_row("🥚 Auto Hatch", lambda: automation.auto_hatch(), row)
            row += 1
            self._create_button_row("💰 Farm Coins", lambda: automation.farm_coins(), row)
        
        elif game_name == "Anime Adventures":
            self._create_option_row("Wave Count:", "waves", ["50", "100", "200", "500", "Infinite"], row)
            row += 1
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard", "Extreme"], row)
            row += 1
            self._create_button_row("🌊 Auto Farm Waves", lambda: automation.auto_farm_waves(int(self.config_vars.get("waves", ctk.StringVar(value="100")).get() or 100)), row)
            row += 1
            self._create_button_row("🎰 Auto Summon", lambda: automation.auto_summon(), row)
            row += 1
            self._create_button_row("⬆ Auto Upgrade Units", lambda: automation.auto_upgrade(), row)
        
        elif game_name == "Bee Swarm Simulator":
            self._create_option_row("Field Type:", "field", ["Sunflower", "Dandelion", "Mushroom", "Blue Flower"], row)
            row += 1
            self._create_button_row("🌸 Collect Pollen", lambda: automation.auto_collect_pollen(), row)
            row += 1
            self._create_button_row("🍯 Convert Honey", lambda: automation.auto_convert_honey(), row)
        
        elif game_name == "Mining Simulator 2":
            self._create_option_row("Ore Type:", "ore", ["Copper", "Iron", "Gold", "Diamond", "Mythic"], row)
            row += 1
            self._create_button_row("⛏ Auto Mine", lambda: automation.auto_mine(self.config_vars.get("ore", ctk.StringVar(value="Copper")).get()), row)
            row += 1
            self._create_button_row("💰 Auto Sell Ores", lambda: automation.auto_sell(), row)
        
        elif game_name == "Adopt Me":
            self._create_option_row("Pet Type:", "pet", ["Common", "Uncommon", "Rare", "Ultra-Rare", "Legendary"], row)
            row += 1
            self._create_button_row("🐾 Auto Age Pets", lambda: automation.auto_age_pets(), row)
            row += 1
            self._create_button_row("🔄 Auto Trade", lambda: automation.auto_trade(), row)
        
        elif game_name == "Clicker Simulator":
            self._create_option_row("CPS:", "cps", ["10", "20", "30", "50", "100"], row)
            row += 1
            self._create_button_row("🖱 Auto Click", lambda: automation.auto_click(int(self.config_vars.get("cps", ctk.StringVar(value="20")).get())), row)
            row += 1
            self._create_button_row("⬆ Auto Rebirth", lambda: automation.auto_rebirth(), row)
        
        elif game_name == "Tapping Legends X":
            self._create_option_row("CPS:", "cps", ["20", "30", "50", "100"], row)
            row += 1
            self._create_button_row("👆 Auto Tap", lambda: automation.auto_tap(int(self.config_vars.get("cps", ctk.StringVar(value="30")).get())), row)
        
        # ========== TOWER DEFENSE ==========
        elif game_name == "All Star Tower Defense":
            self._create_option_row("Wave Count:", "waves", ["50", "100", "200", "Infinite"], row)
            row += 1
            self._create_button_row("🌊 Auto Farm Waves", lambda: automation.auto_wave_farm(), row)
            row += 1
            self._create_button_row("🎰 Auto Summon", lambda: automation.auto_summon(), row)
        
        elif game_name == "Tower Defense Simulator":
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard", "Molten"], row)
            row += 1
            self._create_button_row("🌊 Auto Wave Farm", lambda: automation.auto_wave_farm(), row)
        
        # ========== TYCOON GAMES ==========
        elif game_name == "Restaurant Tycoon 2":
            self._create_option_row("Food Type:", "food", ["Burger", "Pizza", "Sushi", "Dessert"], row)
            row += 1
            self._create_button_row("👨‍🍳 Auto Cook", lambda: automation.auto_cook(), row)
            row += 1
            self._create_button_row("🍽 Auto Serve", lambda: automation.auto_serve(), row)
        
        elif game_name == "Theme Park Tycoon":
            self._create_option_row("Ride Type:", "ride", ["Roller Coaster", "Ferris Wheel", "Carousel"], row)
            row += 1
            self._create_button_row("💰 Auto Collect Money", lambda: automation.auto_collect(), row)
            row += 1
            self._create_button_row("⬆ Auto Upgrade Rides", lambda: automation.auto_upgrade(), row)
        
        # ========== OBBIES ==========
        elif game_name == "Tower of Hell":
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard", "Extreme"], row)
            row += 1
            self._create_button_row("🏃 Auto Complete Tower", lambda: automation.auto_complete(), row)
        
        elif game_name == "Speed Run 4":
            self._create_option_row("Course:", "course", ["Beginner", "Intermediate", "Advanced", "Expert"], row)
            row += 1
            self._create_button_row("🏃 Auto Run Course", lambda: automation.auto_run(), row)
        
        elif game_name == "Evade":
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard"], row)
            row += 1
            self._create_button_row("🏃 Auto Evade", lambda: automation.auto_evade(), row)
        
        # ========== FPS GAMES ==========
        elif game_name == "Arsenal":
            self._create_option_row("Mode:", "mode", ["Standard", "Competitive", "Gun Rotation"], row)
            row += 1
            self._create_button_row("🎯 Auto Aim Assist", lambda: automation.auto_aim(), row)
        
        elif game_name == "Phantom Forces":
            self._create_option_row("Weapon Type:", "weapon", ["Assault Rifle", "SMG", "Sniper", "Pistol"], row)
            row += 1
            self._create_button_row("⚔ Farm Kills", lambda: automation.auto_farm_kills(), row)
        
        # ========== ADVENTURE GAMES ==========
        elif game_name == "Jailbreak":
            self._create_option_row("Rob Location:", "location", ["Bank", "Jewelry Store", "Gas Station", "Museum"], row)
            row += 1
            self._create_button_row("💰 Auto Rob", lambda: automation.auto_rob(self.config_vars.get("location", ctk.StringVar(value="Bank")).get()), row)
            row += 1
            self._create_button_row("🏃 Auto Escape Prison", lambda: automation.auto_escape(), row)
        
        elif game_name == "Mad City":
            self._create_option_row("Rob Type:", "rob", ["Bank", "Jewelry Store", "Gas Station"], row)
            row += 1
            self._create_button_row("💰 Auto Rob", lambda: automation.auto_rob(), row)
        
        elif game_name == "Dragon Adventures":
            self._create_option_row("Dragon Type:", "dragon", ["Common", "Uncommon", "Rare", "Legendary"], row)
            row += 1
            self._create_button_row("🐉 Auto Breed Dragons", lambda: automation.auto_breed(), row)
            row += 1
            self._create_button_row("💰 Farm Coins", lambda: automation.farm_coins(), row)
        
        # ========== LIFE GAMES ==========
        elif game_name == "Welcome to Bloxburg":
            self._create_option_row("Job:", "job", ["Pizza Delivery", "Cashier", "Hairdresser", "Mechanic"], row)
            row += 1
            self._create_button_row("💼 Auto Work", lambda: automation.auto_work(self.config_vars.get("job", ctk.StringVar(value="Pizza Delivery")).get()), row)
        
        elif game_name == "Brookhaven":
            self._create_option_row("Roleplay Type:", "rp", ["Family", "School", "Hospital", "Police"], row)
            row += 1
            self._create_button_row("🎭 Auto Roleplay", lambda: automation.auto_roleplay(), row)
        
        elif game_name == "MeepCity":
            self._create_option_row("Job:", "job", ["Pizza Delivery", "Cashier"], row)
            row += 1
            self._create_button_row("💼 Auto Work", lambda: automation.auto_work(), row)
        
        # ========== SURVIVAL GAMES ==========
        elif game_name == "Natural Disaster Survival":
            self._create_option_row("Disaster Type:", "disaster", ["Tornado", "Flood", "Earthquake", "Blizzard"], row)
            row += 1
            self._create_button_row("🌪 Auto Survive", lambda: automation.auto_survive(), row)
        
        elif game_name == "Zombie Rush":
            self._create_option_row("Wave:", "wave", ["1", "10", "25", "50", "100"], row)
            row += 1
            self._create_button_row("🧟 Kill Zombies", lambda: automation.auto_kill_zombies(), row)
            row += 1
            self._create_button_row("💰 Collect Coins", lambda: automation.auto_collect_coins(), row)
        
        # ========== HORROR GAMES ==========
        elif game_name == "Doors":
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard", "Extreme"], row)
            row += 1
            self._create_button_row("🔓 Auto Solve Puzzles", lambda: automation.auto_solve(), row)
        
        elif game_name == "Rainbow Friends":
            self._create_option_row("Chapter:", "chapter", ["Chapter 1", "Chapter 2", "Chapter 3"], row)
            row += 1
            self._create_button_row("🏃 Auto Escape", lambda: automation.auto_escape(), row)
        
        elif game_name == "Piggy":
            self._create_option_row("Chapter:", "chapter", ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"], row)
            row += 1
            self._create_button_row("🏃 Auto Escape", lambda: automation.auto_escape(), row)
        
        # ========== OTHER GAMES ==========
        elif game_name == "Build A Boat":
            self._create_option_row("Build Type:", "build", ["Speed", "Defense", "Attack"], row)
            row += 1
            self._create_button_row("🚢 Auto Build", lambda: automation.auto_build(), row)
            row += 1
            self._create_button_row("💰 Farm Coins", lambda: automation.farm_coins(), row)
        
        elif game_name == "Murder Mystery 2":
            self._create_option_row("Mode:", "mode", ["Classic", "Assassin", "Hardcore"], row)
            row += 1
            self._create_button_row("🎯 Auto Win", lambda: automation.auto_win(), row)
        
        elif game_name == "Blade Ball":
            self._create_option_row("Difficulty:", "difficulty", ["Easy", "Normal", "Hard"], row)
            row += 1
            self._create_button_row("⚔ Auto Block", lambda: automation.auto_block(), row)
        
        elif game_name == "Rogue Lineage":
            self._create_option_row("Class:", "class", ["Mage", "Warrior", "Assassin"], row)
            row += 1
            self._create_button_row("💫 Farm Mana", lambda: automation.farm_mana(), row)
            row += 1
            self._create_button_row("⚔ Auto Grind", lambda: automation.auto_grind(), row)
        
        elif game_name == "Deepwoken":
            self._create_option_row("Build Type:", "build", ["Mage", "Warrior", "Hybrid"], row)
            row += 1
            self._create_button_row("⬆ Farm Levels", lambda: automation.farm_levels(), row)
        
        elif game_name == "World Zero":
            self._create_option_row("Quest Type:", "quest", ["Main", "Side", "Daily"], row)
            row += 1
            self._create_button_row("📜 Farm Quests", lambda: automation.farm_quests(), row)
        
        elif game_name == "Anime Fighting Simulator":
            self._create_option_row("Training Type:", "training", ["Strength", "Speed", "Chakra"], row)
            row += 1
            self._create_button_row("⚡ Farm Chi", lambda: automation.farm_chi(), row)
            row += 1
            self._create_button_row("💪 Auto Train", lambda: automation.auto_train(), row)
        
        elif game_name == "Grow a Garden":
            # 20+ automation features for Grow a Garden
            self._create_option_row("Seed Type:", "seed", ["Best Available"] + automation.seed_types, row)
            row += 1
            self._create_option_row("Fertilizer Type:", "fertilizer", automation.fertilizer_types, row)
            row += 1
            self._create_option_row("Tool Type:", "tool", automation.tool_types, row)
            row += 1
            self._create_button_row("🌱 Plant Seeds", lambda: automation.plant_seeds(self.config_vars.get("seed", ctk.StringVar(value="Best Available")).get()), row)
            row += 1
            self._create_button_row("💧 Water Plants", lambda: automation.water_plants(), row)
            row += 1
            self._create_button_row("🌾 Harvest Crops", lambda: automation.harvest_crops("All"), row)
            row += 1
            self._create_button_row("🌿 Auto Fertilize", lambda: automation.auto_fertilize(self.config_vars.get("fertilizer", ctk.StringVar(value="Basic")).get()), row)
            row += 1
            self._create_button_row("⬆ Upgrade Garden", lambda: automation.upgrade_garden("Plot Size"), row)
            row += 1
            self._create_button_row("💰 Sell Produce", lambda: automation.sell_produce(), row)
            row += 1
            self._create_button_row("🛒 Buy Seeds", lambda: automation.buy_seeds(self.config_vars.get("seed", ctk.StringVar(value="Best Available")).get()), row)
            row += 1
            self._create_button_row("🌾 Auto Weed", lambda: automation.auto_weed(), row)
            row += 1
            self._create_button_row("🐛 Pest Control", lambda: automation.auto_pest_control(), row)
            row += 1
            self._create_button_row("♻ Auto Compost", lambda: automation.auto_compost(), row)
            row += 1
            self._create_button_row("💦 Auto Irrigate", lambda: automation.auto_irrigate(), row)
            row += 1
            self._create_button_row("✂ Auto Prune", lambda: automation.auto_prune(), row)
            row += 1
            self._create_button_row("🌾 Harvest All", lambda: automation.auto_harvest_all(), row)
            row += 1
            self._create_button_row("🌱 Plant All Plots", lambda: automation.auto_plant_all(self.config_vars.get("seed", ctk.StringVar(value="Best Available")).get()), row)
            row += 1
            self._create_button_row("🔧 Upgrade Tools", lambda: automation.auto_upgrade_tools(self.config_vars.get("tool", ctk.StringVar(value="All")).get()), row)
            row += 1
            self._create_button_row("📋 Complete Orders", lambda: automation.auto_complete_orders(), row)
            row += 1
            self._create_button_row("🎁 Collect Rewards", lambda: automation.auto_collect_rewards(), row)
            row += 1
            self._create_button_row("📦 Manage Inventory", lambda: automation.auto_manage_inventory(), row)
            row += 1
            self._create_button_row("📐 Optimize Layout", lambda: automation.auto_optimize_layout(), row)
            row += 1
            self._create_button_row("🔄 Full Auto Cycle", lambda: automation.full_auto_cycle(), row)
        
        else:
            # Fallback for any unlisted games
            self._create_option_row("Automation Mode:", "mode", ["Farming", "Grinding", "Collecting"], row)
            row += 1
            self._create_button_row("▶ Start Generic Automation", lambda: automation.start_farming({}), row)
    
    def _start_blox_fruits(self):
        """Start Blox Fruits automation"""
        automation = self.game_manager.get_automation("Blox Fruits")
        config = {
            "fruit_type": self.config_vars.get("fruit", ctk.StringVar(value="Any")).get(),
            "location": self.config_vars.get("location", ctk.StringVar(value="First Sea")).get()
        }
        automation.farm_fruits(config["fruit_type"], config["location"])
        self.current_automation = automation
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0.5)
        self.progress_label.configure(text="Status: Running - Blox Fruits", text_color="green")
        self.main_window.update_status("Blox Fruits automation started", "success")
    
    def _start_da_hood(self):
        """Start Da Hood automation"""
        automation = self.game_manager.get_automation("Da Hood")
        auto_type = self.config_vars.get("type", ctk.StringVar(value="Cash Farm")).get()
        if auto_type == "Cash Farm":
            automation.auto_farm_cash()
        elif auto_type == "Auto Duel":
            automation.auto_duel()
        else:
            automation.auto_rob()
        self.current_automation = automation
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0.5)
        self.progress_label.configure(text="Status: Running - Da Hood", text_color="green")
        self.main_window.update_status("Da Hood automation started", "success")
    
    def _create_option_row(self, label_text: str, var_key: str, options: list, row: int):
        """Create a labeled option row"""
        frame = ctk.CTkFrame(self.options_scroll, corner_radius=5)
        frame.pack(fill="x", padx=10, pady=5)
        frame.grid_columnconfigure(1, weight=1)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=12),
            width=120,
            anchor="w"
        )
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        var = ctk.StringVar(value=options[0] if options else "")
        self.config_vars[var_key] = var
        
        combo = ctk.CTkComboBox(
            frame,
            values=options,
            variable=var,
            width=200,
            font=ctk.CTkFont(size=11)
        )
        combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def _create_button_row(self, button_text: str, command, row: int):
        """Create a button row with automation tracking"""
        frame = ctk.CTkFrame(self.options_scroll, corner_radius=5)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Wrap command to update UI state
        def wrapped_command():
            try:
                command()
                # Update UI state after command execution
                game_name = self.game_var.get()
                automation = self.game_manager.get_automation(game_name)
                self.current_automation = automation
                self.start_btn.configure(state="disabled")
                self.pause_btn.configure(state="normal")
                self.stop_btn.configure(state="normal")
                self.progress_bar.set(0.5)
                self.progress_label.configure(text=f"Status: Running - {game_name}", text_color="green")
                self.main_window.update_status(f"{button_text} started for {game_name}", "success")
            except Exception as e:
                logger.error(f"Error executing automation: {e}")
                self.main_window.update_status(f"Error: {str(e)}", "error")
        
        button = ctk.CTkButton(
            frame,
            text=button_text,
            command=wrapped_command,
            width=200,
            font=ctk.CTkFont(size=11),
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        button.pack(padx=10, pady=10)
    
    def on_game_change(self, value):
        """Handle game selection change"""
        self._create_game_options()
        self.main_window.update_status(f"Selected game: {value}", "info")
    
    def start_automation(self):
        """Start automation for any game"""
        game_name = self.game_var.get()
        automation = self.game_manager.get_automation(game_name)
        
        # Most games use button-based automation, but some use the main Start button
        # This handles games that don't have specific button handlers
        
        # Games that use generic start_farming
        generic_games = [
            "King Legacy", "Project Slayers", "Shindo Life", "Ninja Legends",
            "Super Power Fighting Simulator", "Your Bizarre Adventure", "A One Piece Game",
            "Grand Piece Online", "Slap Battles", "Ability Wars", "Pet Simulator 99",
            "Bee Swarm Simulator", "Mining Simulator 2", "Adopt Me", "Clicker Simulator",
            "Tapping Legends X", "All Star Tower Defense", "Tower Defense Simulator",
            "Restaurant Tycoon 2", "Theme Park Tycoon", "Tower of Hell", "Speed Run 4",
            "Evade", "Arsenal", "Phantom Forces", "Mad City", "Dragon Adventures",
            "Welcome to Bloxburg", "Brookhaven", "MeepCity", "Natural Disaster Survival",
            "Zombie Rush", "Doors", "Rainbow Friends", "Piggy", "Build A Boat",
            "Murder Mystery 2", "Blade Ball", "Rogue Lineage", "Deepwoken", "World Zero",
            "Anime Fighting Simulator", "Grow a Garden"
        ]
        
        if game_name in generic_games:
            automation.start_farming({})
            self.current_automation = automation
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self.stop_btn.configure(state="normal")
            self.progress_bar.set(0.5)
            self.progress_label.configure(text=f"Status: Running - {game_name}", text_color="green")
            self.main_window.update_status(f"Automation started: {game_name}", "success")
        else:
            # Games with specific handlers (Blox Fruits, Da Hood, etc. use button handlers)
            self.main_window.update_status(f"Use the specific automation buttons for {game_name}", "info")
    
    def pause_automation(self):
        """Pause automation"""
        if self.current_automation:
            self.current_automation.engine.pause_automation()
            self.pause_btn.configure(state="disabled")
            self.progress_label.configure(text="Status: Paused", text_color="orange")
            self.main_window.update_status("Automation paused", "warning")
    
    def stop_automation(self):
        """Stop automation"""
        if self.current_automation:
            self.current_automation.engine.stop_automation()
            self.current_automation = None
            self.start_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")
            self.stop_btn.configure(state="disabled")
            self.progress_bar.set(0)
            self.progress_label.configure(text="Status: Idle", text_color="gray")
            self.main_window.update_status("Automation stopped", "info")
    
    def _update_stats(self):
        """Update statistics display"""
        if self.current_automation:
            stats = self.current_automation.engine.get_stats()
            runtime = stats['runtime']
            actions = stats['actions_performed']
            errors = stats['errors']
            
            # Update progress bar based on actions
            if actions > 0:
                progress = min(0.9, actions / 1000.0)  # Cap at 90% for visual
                self.progress_bar.set(progress)
            
            self.stats_label.configure(
                text=f"Runtime: {runtime}s | Actions: {actions} | Errors: {errors}"
            )
        self.parent.after(1000, self._update_stats)
