"""
Main Window - The central widget of the application
"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QScrollArea, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.ui.widgets.flip_clock import FlipClock
from src.ui.widgets.reminders_panel import RemindersPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock and Remind - English Learning")
        self.setGeometry(100, 100, 1100, 1200)
        self.setMinimumSize(900, 950)
        
        # Position window at top-right corner of screen
        self.position_top_right()
        
        # Set main stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }
        """)
        
        # Create scroll area for responsiveness
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: white;")
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # Title
        title = QLabel("⏰ Clock and Remind")
        title_font = QFont("Segoe UI", 28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #667eea; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Learn English with Style")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        
        # Flip Clock widget
        self.flip_clock = FlipClock()
        main_layout.addWidget(self.flip_clock)
        
        # Reminders Panel
        self.reminders_panel = RemindersPanel()
        main_layout.addWidget(self.reminders_panel, 1)  # Give stretch factor
        
        # Add stretch to push everything to top
        main_layout.addStretch()
    
    def position_top_right(self):
        """Position window at top-right corner of screen"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.availableGeometry()
            # Calculate position: right edge - window width, top edge + small margin
            x = screen_geo.right() - self.width() - 10
            y = screen_geo.top() + 10
            self.move(x, y)
