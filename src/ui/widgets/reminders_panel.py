"""
Reminders Panel Widget - Displays and manages reminders
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QCheckBox, QPushButton, QTimeEdit, 
                             QScrollArea, QDialog, QLineEdit, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTime, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor
from src.models.reminder import Reminder
from src.services.notification_service import NotificationService


class AddReminderDialog(QDialog):
    """Custom styled dialog for adding new reminder"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Reminder")
        self.setFixedSize(400, 320)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        # Main container with shadow
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Container widget
        container = QWidget()
        container.setObjectName("dialogContainer")
        container.setStyleSheet("""
            #dialogContainer {
                background: #1a1a2e;
                border-radius: 16px;
                border: 2px solid #4a7adb;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 100))
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(25, 20, 25, 25)
        container_layout.setSpacing(20)
        
        # Header with title and close button
        header = QHBoxLayout()
        
        title = QLabel("⏰ New Reminder")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        header.addWidget(title)
        
        header.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 16px;
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #f44336;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.reject)
        header.addWidget(close_btn)
        
        container_layout.addLayout(header)
        
        # Time input section
        time_section = QVBoxLayout()
        time_section.setSpacing(8)
        
        time_label = QLabel("Select Time")
        time_label.setFont(QFont("Segoe UI", 11))
        time_label.setStyleSheet("color: #a0a0a0; background: transparent;")
        time_section.addWidget(time_label)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm AP")
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setFont(QFont("Segoe UI", 14))
        self.time_edit.setMinimumHeight(50)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background: #252542;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
            }
            QTimeEdit:focus {
                border: 2px solid #667eea;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                background: #3a3a5a;
                border: none;
                width: 25px;
                border-radius: 5px;
            }
            QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
                background: #667eea;
            }
            QTimeEdit::up-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid white;
                width: 0;
                height: 0;
            }
            QTimeEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                width: 0;
                height: 0;
            }
        """)
        time_section.addWidget(self.time_edit)
        
        container_layout.addLayout(time_section)
        
        # Content input section
        content_section = QVBoxLayout()
        content_section.setSpacing(8)
        
        content_label = QLabel("Reminder Content")
        content_label.setFont(QFont("Segoe UI", 11))
        content_label.setStyleSheet("color: #a0a0a0; background: transparent;")
        content_section.addWidget(content_label)
        
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("e.g., Practice English speaking...")
        self.content_input.setFont(QFont("Segoe UI", 13))
        self.content_input.setMinimumHeight(50)
        self.content_input.setStyleSheet("""
            QLineEdit {
                background: #252542;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                color: white;
                padding: 10px 15px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
            QLineEdit::placeholder {
                color: #666;
            }
        """)
        content_section.addWidget(self.content_input)
        
        container_layout.addLayout(content_section)
        
        container_layout.addStretch()
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                color: #a0a0a0;
                padding: 10px 25px;
            }
            QPushButton:hover {
                border-color: #667eea;
                color: white;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("✓ Add Reminder")
        add_btn.setMinimumHeight(45)
        add_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                border: none;
                border-radius: 10px;
                color: white;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background: #5a6fd6;
            }
        """)
        add_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(add_btn)
        
        container_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(container)
    
    def get_time(self) -> QTime:
        """Get selected time"""
        return self.time_edit.time()
    
    def get_content(self) -> str:
        """Get reminder content"""
        return self.content_input.text().strip()
    
    def mousePressEvent(self, event):
        """Allow dragging the dialog"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle dialog dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()


class ReminderItem(QWidget):
    """Individual reminder item widget"""
    
    remove_clicked = pyqtSignal(object)
    
    # Color palette for different reminders
    COLORS = ['#4a7adb', '#f5a623', '#4caf50', '#e74c3c', '#9b59b6', '#1abc9c']
    _color_index = 0
    
    def __init__(self, reminder: Reminder, color: str = None):
        super().__init__()
        self.reminder = reminder
        # Assign color based on index or use provided color
        if color:
            self.border_color = color
        else:
            self.border_color = ReminderItem.COLORS[ReminderItem._color_index % len(ReminderItem.COLORS)]
            ReminderItem._color_index += 1
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setMinimumHeight(80)
        self.setMaximumHeight(90)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Left border indicator (using a vertical line widget)
        border_indicator = QWidget()
        border_indicator.setFixedWidth(4)
        border_indicator.setStyleSheet(f"background: {self.border_color}; border-radius: 2px;")
        layout.addWidget(border_indicator)
        
        # Time and content (left side)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        
        # Time label with color matching border
        self.time_label = QLabel(self.reminder.time.toString("hh:mm AP"))
        time_font = QFont("Segoe UI", 13)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        self.time_label.setStyleSheet(f"color: {self.border_color}; background: transparent;")
        text_layout.addWidget(self.time_label)
        
        # Content label
        self.content_label = QLabel(self.reminder.content)
        content_font = QFont("Segoe UI", 12)
        self.content_label.setFont(content_font)
        self.content_label.setStyleSheet("color: #333; background: transparent;")
        text_layout.addWidget(self.content_label)
        
        layout.addLayout(text_layout, 1)
        
        # Checkbox on the right side
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.reminder.completed)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        self.checkbox.setFixedSize(28, 28)
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_checkbox_style()
        layout.addWidget(self.checkbox)
        
        # Set card styling
        self.setStyleSheet("""
            ReminderItem {
                background: white;
                border-radius: 12px;
            }
        """)
        
        self.update_completed_style()
    
    def update_checkbox_style(self):
        """Update checkbox style based on state"""
        if self.reminder.completed:
            self.checkbox.setStyleSheet("""
                QCheckBox::indicator {
                    width: 24px;
                    height: 24px;
                    border-radius: 6px;
                    background: #4caf50;
                    border: 2px solid #4caf50;
                }
                QCheckBox::indicator:checked {
                    image: none;
                }
            """)
        else:
            self.checkbox.setStyleSheet(f"""
                QCheckBox::indicator {{
                    width: 24px;
                    height: 24px;
                    border-radius: 6px;
                    background: transparent;
                    border: 2px solid {self.border_color};
                }}
                QCheckBox::indicator:hover {{
                    border: 2px solid {self.border_color};
                    background: rgba(74, 122, 219, 0.1);
                }}
            """)
    
    def update_completed_style(self):
        """Update style based on completion status"""
        if self.reminder.completed:
            self.content_label.setStyleSheet("""
                color: #999; 
                background: transparent;
                text-decoration: line-through;
            """)
            self.time_label.setStyleSheet("color: #999; background: transparent;")
        else:
            self.content_label.setStyleSheet("color: #333; background: transparent;")
            self.time_label.setStyleSheet(f"color: {self.border_color}; background: transparent;")
    
    def on_checkbox_changed(self):
        """Handle checkbox state change"""
        self.reminder.completed = self.checkbox.isChecked()
        self.update_checkbox_style()
        self.update_completed_style()


class RemindersPanel(QWidget):
    """Panel displaying all reminders"""
    
    def __init__(self):
        super().__init__()
        self.reminders = []
        self.triggered_reminders = set()  # Track already triggered reminders
        self.notification_service = NotificationService()
        self.init_ui()
        self.load_reminders()
        self.start_reminder_checker()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(12)
        
        # Set background
        self.setStyleSheet("background: #f8f9fa;")
        
        # Title
        title = QLabel("📋 Daily Reminders")
        title_font = QFont("Segoe UI", 18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #333; padding: 10px 0px; font-weight: bold; background: transparent;")
        layout.addWidget(title)
        
        # Scroll area for reminders
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 6px;
                background: transparent;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #ccc;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.reminders_container = QWidget()
        self.reminders_layout = QVBoxLayout(self.reminders_container)
        self.reminders_layout.setContentsMargins(5, 5, 5, 5)
        self.reminders_layout.setSpacing(12)
        self.reminders_container.setStyleSheet("background: transparent;")
        
        # Add stretch at bottom to push items up
        self.reminders_layout.addStretch()
        
        scroll.setWidget(self.reminders_container)
        layout.addWidget(scroll, 1)  # Give scroll area stretch factor
        
        # Add New Reminder Button
        add_btn = QPushButton("+ Add New Reminder")
        add_btn.setMinimumHeight(50)
        add_btn.setMaximumHeight(50)
        add_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6fd6;
            }
            QPushButton:pressed {
                background-color: #4a5fc6;
            }
        """)
        add_btn.clicked.connect(self.add_reminder_dialog)
        layout.addWidget(add_btn)
    
    def load_reminders(self):
        """Load default reminders with different colors"""
        # Reset color index
        ReminderItem._color_index = 0
        
        default_reminders = [
            (Reminder(QTime(8, 0), "Learn 10 new words"), "#4a7adb"),      # Blue
            (Reminder(QTime(12, 0), "Practice pronunciation"), "#f5a623"),  # Orange/Yellow
            (Reminder(QTime(15, 0), "Grammar exercise"), "#4caf50"),        # Green
            (Reminder(QTime(19, 0), "Review vocabulary"), "#e74c3c"),       # Red
        ]
        
        for reminder, color in default_reminders:
            self.add_reminder(reminder, color)
    
    def add_reminder(self, reminder: Reminder, color: str = None):
        """Add a reminder to the panel"""
        self.reminders.append(reminder)
        item = ReminderItem(reminder, color)
        item.remove_clicked.connect(self.remove_reminder)
        # Insert before the stretch
        self.reminders_layout.insertWidget(self.reminders_layout.count() - 1, item)
    
    def remove_reminder(self, reminder: Reminder):
        """Remove a reminder"""
        if reminder in self.reminders:
            self.reminders.remove(reminder)
            self.refresh_reminders()
    
    def refresh_reminders(self):
        """Refresh the reminders display"""
        # Remove all widgets except the stretch at the end
        while self.reminders_layout.count() > 1:
            item = self.reminders_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        # Reset color index
        ReminderItem._color_index = 0
        
        for reminder in sorted(self.reminders, key=lambda r: r.time.msecsSinceStartOfDay()):
            item = ReminderItem(reminder)
            item.remove_clicked.connect(self.remove_reminder)
            # Insert before the stretch
            self.reminders_layout.insertWidget(self.reminders_layout.count() - 1, item)
    
    def add_reminder_dialog(self):
        """Show dialog to add a new reminder"""
        dialog = AddReminderDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            content = dialog.get_content()
            if content:
                reminder_time = dialog.get_time()
                reminder = Reminder(reminder_time, content)
                self.add_reminder(reminder)
                self.refresh_reminders()
    
    def start_reminder_checker(self):
        """Start timer to check for due reminders"""
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_reminders)
        self.check_timer.start(1000)  # Check every second
    
    def check_reminders(self):
        """Check if any reminder is due and show notification"""
        current_time = QTime.currentTime()
        current_key = current_time.toString("hh:mm")
        
        for reminder in self.reminders:
            if reminder.completed:
                continue
                
            reminder_key = reminder.time.toString("hh:mm")
            # Create unique key for this reminder instance
            unique_key = f"{reminder_key}_{reminder.content}"
            
            # Check if time matches and not already triggered
            if reminder_key == current_key and unique_key not in self.triggered_reminders:
                self.triggered_reminders.add(unique_key)
                self.show_reminder_notification(reminder)
    
    def show_reminder_notification(self, reminder: Reminder):
        """Show notification for a reminder"""
        time_str = reminder.time.toString("hh:mm AP")
        self.notification_service.show_notification(
            time_str, 
            reminder.content,
            self.window()
        )
