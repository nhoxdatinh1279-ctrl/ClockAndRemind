"""
Notification Service - Handles reminder notifications with sound and popup
"""

import os
import winsound
import threading
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QColor

# Try to import pygame for audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class NotificationDialog(QDialog):
    """Beautiful notification popup for reminders"""
    
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.title_text = title
        self.message_text = message
        self.sound_playing = False
        self.init_ui()
        self.init_sound()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Reminder")
        self.setFixedSize(420, 220)
        self.setWindowFlags(
            Qt.WindowType.Dialog | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Container
        container = QLabel()
        container.setObjectName("notifContainer")
        container.setStyleSheet("""
            #notifContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
            }
        """)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 15)
        shadow.setColor(QColor(102, 126, 234, 150))
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(25, 20, 25, 20)
        container_layout.setSpacing(12)
        
        # Header with icon and close button
        header = QHBoxLayout()
        
        # Bell icon and title
        icon_title = QHBoxLayout()
        icon_title.setSpacing(10)
        
        bell_icon = QLabel("🔔")
        bell_icon.setFont(QFont("Segoe UI Emoji", 24))
        bell_icon.setStyleSheet("background: transparent;")
        icon_title.addWidget(bell_icon)
        
        title_label = QLabel("Time for English!")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
        icon_title.addWidget(title_label)
        icon_title.addStretch()
        
        header.addLayout(icon_title)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.2);
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.3);
            }
        """)
        close_btn.clicked.connect(self.close_notification)
        header.addWidget(close_btn)
        
        container_layout.addLayout(header)
        
        # Time display
        time_label = QLabel(self.title_text)
        time_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        time_label.setStyleSheet("color: white; background: transparent;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(time_label)
        
        # Message
        msg_label = QLabel(self.message_text)
        msg_label.setFont(QFont("Segoe UI", 14))
        msg_label.setStyleSheet("color: rgba(255,255,255,0.95); background: transparent;")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        container_layout.addWidget(msg_label)
        
        container_layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        # Snooze button
        snooze_btn = QPushButton("⏰ Snooze 5 min")
        snooze_btn.setMinimumHeight(40)
        snooze_btn.setFont(QFont("Segoe UI", 11))
        snooze_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        snooze_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.2);
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                color: white;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.3);
                border-color: rgba(255,255,255,0.5);
            }
        """)
        snooze_btn.clicked.connect(self.snooze)
        btn_layout.addWidget(snooze_btn)
        
        # Dismiss button
        dismiss_btn = QPushButton("✓ Got it!")
        dismiss_btn.setMinimumHeight(40)
        dismiss_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        dismiss_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dismiss_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border: none;
                border-radius: 10px;
                color: #667eea;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        dismiss_btn.clicked.connect(self.close_notification)
        btn_layout.addWidget(dismiss_btn)
        
        container_layout.addLayout(btn_layout)
        
        main_layout.addWidget(container)
        
        # Position at top-right corner of screen
        self.position_on_screen()
        
        # Auto-close timer (30 seconds)
        self.auto_close_timer = QTimer(self)
        self.auto_close_timer.timeout.connect(self.close_notification)
        self.auto_close_timer.start(30000)
    
    def init_sound(self):
        """Initialize and play notification sound"""
        try:
            # Get the app root directory
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sound_file = os.path.join(base_path, "assets", "sounds", "notification.mp3")
            
            if os.path.exists(sound_file) and PYGAME_AVAILABLE:
                # Use pygame to play sound in a separate thread
                def play_sound():
                    try:
                        pygame.mixer.music.load(sound_file)
                        pygame.mixer.music.set_volume(0.8)
                        pygame.mixer.music.play()
                        self.sound_playing = True
                    except Exception as e:
                        print(f"Pygame error: {e}")
                
                threading.Thread(target=play_sound, daemon=True).start()
            else:
                # Fallback: Use Windows default notification sound
                winsound.PlaySound("SystemExclamation", 
                                   winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Error playing sound: {e}")
            # Fallback to simple beep
            try:
                winsound.Beep(800, 200)
                winsound.Beep(1000, 200)
                winsound.Beep(1200, 300)
            except:
                pass
    
    def stop_sound(self):
        """Stop playing sound"""
        if PYGAME_AVAILABLE and self.sound_playing:
            try:
                pygame.mixer.music.stop()
                self.sound_playing = False
            except:
                pass
    
    def position_on_screen(self):
        """Position dialog at top-right corner of screen"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.availableGeometry()
            x = screen_geo.right() - self.width() - 20
            y = screen_geo.top() + 20
            self.move(x, y)
    
    def snooze(self):
        """Snooze the reminder for 5 minutes"""
        self.snoozed = True
        self.close_notification()
    
    def close_notification(self):
        """Close the notification and stop sound"""
        self.stop_sound()
        self.auto_close_timer.stop()
        self.accept()
    
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


class NotificationService:
    """Service to manage reminder notifications"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_notifications = []
        return cls._instance
    
    def show_notification(self, time_str: str, content: str, parent=None):
        """Show a notification popup"""
        dialog = NotificationDialog(time_str, content, parent)
        dialog.show()
        self.active_notifications.append(dialog)
        return dialog
    
    def close_all(self):
        """Close all active notifications"""
        for notif in self.active_notifications:
            try:
                notif.close()
            except:
                pass
        self.active_notifications.clear()
