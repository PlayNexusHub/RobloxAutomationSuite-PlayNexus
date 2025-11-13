"""
Macro and Clicker Module
Automated clicking and macro functionality
"""

import logging
import time
import threading
import pyautogui
from typing import Dict, Any, Optional, Tuple
from core.automation_engine import AutomationEngine

logger = logging.getLogger(__name__)

class MacroClicker:
    """Macro and clicker automation"""
    
    def __init__(self):
        self.engine = AutomationEngine()
        self.click_positions: list = []
        self.is_clicking = False
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def start_clicking(self, config: Dict[str, Any]) -> bool:
        """
        Start automated clicking
        
        Args:
            config: Configuration dict with:
                - position: (x, y) tuple or "current" for current mouse position
                - interval: Time between clicks in seconds
                - clicks_per_second: Alternative to interval
                - duration: How long to click (None for infinite)
                - button: "left" or "right"
        """
        try:
            position = config.get("position", "current")
            if position == "current":
                position = pyautogui.position()
            
            interval = config.get("interval")
            if not interval:
                cps = config.get("clicks_per_second", 10)
                interval = 1.0 / cps
            
            task_config = {
                "type": "clicker",
                "position": position,
                "interval": interval,
                "duration": config.get("duration"),
                "button": config.get("button", "left"),
                "delay": interval
            }
            
            self.is_clicking = True
            return self.engine.start_automation(task_config, self._click_callback)
        except Exception as e:
            logger.error(f"Error starting clicker: {e}")
            return False
    
    def stop_clicking(self) -> bool:
        """Stop automated clicking"""
        self.is_clicking = False
        return self.engine.stop_automation()
    
    def _click_callback(self, stats: Dict[str, Any]):
        """Callback for click updates"""
        pass
    
    def record_click_position(self) -> Tuple[int, int]:
        """Record current mouse position"""
        pos = pyautogui.position()
        self.click_positions.append(pos)
        logger.info(f"Recorded click position: {pos}")
        return pos
    
    def clear_positions(self):
        """Clear recorded positions"""
        self.click_positions.clear()

class MacroRecorder:
    """Records and plays back macros"""
    
    def __init__(self):
        self.is_recording = False
        self.macro_actions: list = []
        self.start_time: Optional[float] = None
        
    def start_recording(self):
        """Start recording macro"""
        self.is_recording = True
        self.macro_actions = []
        self.start_time = time.time()
        logger.info("Macro recording started")
    
    def stop_recording(self):
        """Stop recording macro"""
        self.is_recording = False
        logger.info(f"Macro recording stopped. Recorded {len(self.macro_actions)} actions")
    
    def record_action(self, action_type: str, data: Dict[str, Any]):
        """Record an action"""
        if self.is_recording:
            timestamp = time.time() - (self.start_time or 0)
            self.macro_actions.append({
                "type": action_type,
                "timestamp": timestamp,
                "data": data
            })
    
    def play_macro(self, actions: Optional[list] = None) -> bool:
        """Play back a macro"""
        actions_to_play = actions or self.macro_actions
        if not actions_to_play:
            logger.warning("No macro actions to play")
            return False
        
        try:
            for action in actions_to_play:
                action_type = action.get("type")
                data = action.get("data", {})
                
                if action_type == "click":
                    pyautogui.click(data.get("x"), data.get("y"), button=data.get("button", "left"))
                elif action_type == "key":
                    pyautogui.press(data.get("key"))
                elif action_type == "move":
                    pyautogui.moveTo(data.get("x"), data.get("y"))
                elif action_type == "delay":
                    time.sleep(data.get("duration", 0.1))
                
                # Wait for next action timing
                if action != actions_to_play[-1]:
                    next_action = actions_to_play[actions_to_play.index(action) + 1]
                    delay = next_action.get("timestamp", 0) - action.get("timestamp", 0)
                    if delay > 0:
                        time.sleep(delay)
            
            logger.info("Macro playback completed")
            return True
        except Exception as e:
            logger.error(f"Error playing macro: {e}")
            return False
    
    def save_macro(self, file_path: str) -> bool:
        """Save macro to file"""
        import json
        try:
            with open(file_path, 'w') as f:
                json.dump(self.macro_actions, f, indent=2)
            logger.info(f"Macro saved to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving macro: {e}")
            return False
    
    def load_macro(self, file_path: str) -> bool:
        """Load macro from file"""
        import json
        try:
            with open(file_path, 'r') as f:
                self.macro_actions = json.load(f)
            logger.info(f"Macro loaded from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading macro: {e}")
            return False

