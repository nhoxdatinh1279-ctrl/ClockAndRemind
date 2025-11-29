"""
Reminder Model - Data model for reminders
"""

from PyQt6.QtCore import QTime
from dataclasses import dataclass


@dataclass
class Reminder:
    """Reminder data model"""
    time: QTime
    content: str
    completed: bool = False
    
    def to_dict(self):
        """Convert reminder to dictionary"""
        return {
            "time": self.time.toString("hh:mm"),
            "content": self.content,
            "completed": self.completed
        }
    
    @staticmethod
    def from_dict(data):
        """Create reminder from dictionary"""
        time = QTime.fromString(data["time"], "hh:mm")
        return Reminder(
            time=time,
            content=data["content"],
            completed=data.get("completed", False)
        )
