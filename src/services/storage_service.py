"""
Storage Service - Handles saving and loading reminders to/from JSON file
"""

import json
import os
from datetime import date
from typing import List
from src.models.reminder import Reminder


class StorageService:
    """Service for persisting reminders to JSON file"""
    
    def __init__(self, filename: str = "reminders.json"):
        # Get the directory where the app is running
        self.app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(self.app_dir, "data")
        self.filepath = os.path.join(self.data_dir, filename)
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_reminders(self, reminders: List[Reminder]) -> bool:
        """Save reminders to JSON file"""
        try:
            data = {
                "last_saved": date.today().isoformat(),
                "reminders": [r.to_dict() for r in reminders]
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving reminders: {e}")
            return False
    
    def load_reminders(self) -> tuple[List[Reminder], bool]:
        """
        Load reminders from JSON file.
        Returns tuple of (reminders list, is_new_day flag)
        """
        try:
            if not os.path.exists(self.filepath):
                return [], False
            
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            reminders = [Reminder.from_dict(r) for r in data.get("reminders", [])]
            
            # Check if it's a new day
            last_saved = data.get("last_saved")
            is_new_day = False
            if last_saved:
                last_date = date.fromisoformat(last_saved)
                is_new_day = last_date < date.today()
            
            # Reset daily reminders if new day
            if is_new_day:
                for reminder in reminders:
                    reminder.reset_for_new_day()
            
            return reminders, is_new_day
            
        except Exception as e:
            print(f"Error loading reminders: {e}")
            return [], False
    
    def has_saved_data(self) -> bool:
        """Check if there's existing saved data"""
        return os.path.exists(self.filepath)
