"""
Reminder Model - Data model for reminders
"""

import uuid
from PyQt6.QtCore import QTime
from dataclasses import dataclass, field


@dataclass
class Reminder:
    """Reminder data model"""
    time: QTime
    content: str
    completed: bool = False
    repeat_daily: bool = True  # Lặp lại hàng ngày
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self):
        """Convert reminder to dictionary"""
        return {
            "id": self.id,
            "time": self.time.toString("hh:mm"),
            "content": self.content,
            "completed": self.completed,
            "repeat_daily": self.repeat_daily
        }
    
    @staticmethod
    def from_dict(data):
        """Create reminder from dictionary"""
        time = QTime.fromString(data["time"], "hh:mm")
        return Reminder(
            time=time,
            content=data["content"],
            completed=data.get("completed", False),
            repeat_daily=data.get("repeat_daily", True),
            id=data.get("id", str(uuid.uuid4()))
        )
    
    def reset_for_new_day(self):
        """Reset completed status for new day if repeat_daily is True"""
        if self.repeat_daily:
            self.completed = False
