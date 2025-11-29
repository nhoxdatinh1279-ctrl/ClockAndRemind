"""
Flip Clock Widget - Displays time in flip clock style with animation
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGraphicsOpacityEffect, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QEasingCurve, QRect, QVariantAnimation
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPixmap, QTransform, QPen, QBrush, QPainterPath
from datetime import datetime


class BlinkingSeparator(QLabel):
    """Colon separator with blinking effect"""
    
    def __init__(self):
        super().__init__(":")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                color: #4a7adb;
                font-size: 48px;
                font-weight: bold;
                margin: 0 0px;
            }
        """)
        self.setMinimumWidth(15)
        self.visible_state = True
        
        # Setup opacity effect for blinking
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        # Opacity animation for blinking
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_visibility)
        self.blink_timer.start(500)  # Blink every 500ms
    
    def toggle_visibility(self):
        """Toggle visibility for blinking effect"""
        self.visible_state = not self.visible_state
        opacity = 1.0 if self.visible_state else 0.3
        self.opacity_effect.setOpacity(opacity)


class FlipNumberWidget(QWidget):
    """Flip number display with real flip animation"""
    
    def __init__(self, initial_value="00"):
        super().__init__()
        self.current_value = initial_value
        self.next_value = initial_value
        self.flip_progress = 0.0
        self.is_flipping = False
        
        # Font styling - will be updated dynamically
        self.font_display = QFont("Courier New", 64, QFont.Weight.Bold)
        self.base_font_size = 64
        
        # Setup animation timer
        self.flip_timer = QTimer()
        self.flip_timer.timeout.connect(self.update_flip_animation)
        
        # Set size only (no stylesheet to avoid conflicts)
        self.setMinimumSize(130, 300)
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(size_policy)
    
    def resizeEvent(self, a0):
        """Dynamically adjust font size based on widget size"""
        super().resizeEvent(a0)
        # Calculate font size proportional to widget height (increased for better visibility)
        new_font_size = max(30, int(self.height() * 0.5))
        self.font_display.setPointSize(new_font_size)
    
    def update_flip_animation(self):
        """Update flip animation progress"""
        if self.is_flipping:
            self.flip_progress += 0.06  # Speed of flip
            if self.flip_progress >= 1.0:
                self.flip_progress = 1.0
                self.is_flipping = False
                self.current_value = self.next_value
                self.flip_timer.stop()
            self.update()
    
    def paintEvent(self, a0):
        """Draw flip animation with centered number"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Create rounded rectangle path for background
        path = QPainterPath()
        path.addRoundedRect(1, 1, width - 2, height - 2, 12, 12)
        
        # Draw filled rounded background
        painter.fillPath(path, QColor("#1a1a1a"))
        
        # Draw rounded border
        border_pen = QPen(QColor("#4a7adb"))
        border_pen.setWidth(3)
        painter.setPen(border_pen)
        painter.drawPath(path)
        
        # Calculate flip angle (0 to 180 degrees)
        flip_angle = self.flip_progress * 180.0
        
        painter.setFont(self.font_display)
        painter.setPen(QColor("#ffffff"))
        
        # Create text rect with padding to avoid clipping
        text_rect = QRect(15, 15, width - 30, height - 30)
        
        # Current number - scales down and rotates as it flips (first half)
        if flip_angle < 90:
            scale_y = 1.0 - (flip_angle / 90.0)
            
            painter.save()
            # Move to center, scale on Y axis, move back
            painter.translate(center_x, center_y)
            painter.scale(1.0, scale_y)
            painter.translate(-center_x, -center_y)
            
            # Draw centered text
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.current_value)
            
            # Draw top half clip (only show top half during first flip)
            painter.restore()
        
        # Next number - scales up and rotates as it flips (second half)
        if flip_angle > 90:
            scale_y = (flip_angle - 90.0) / 90.0
            
            painter.save()
            # Move to center, scale on Y axis, move back
            painter.translate(center_x, center_y)
            painter.scale(1.0, scale_y)
            painter.translate(-center_x, -center_y)
            
            # Draw centered text
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.next_value)
            
            painter.restore()
        
        # Draw divider line in the middle (always visible)
        painter.setPen(QColor("#444444"))
        painter.drawLine(0, int(center_y), width, int(center_y))
    
    def animate_flip(self, new_value):
        """Animate flip when value changes"""
        new_value_str = str(new_value).zfill(2)
        
        if new_value_str != self.current_value:
            self.next_value = new_value_str
            self.is_flipping = True
            self.flip_progress = 0.0
            
            # Start animation timer
            self.flip_timer.start(30)  # 30ms interval
    
    def update_value_instant(self, value):
        """Update value without animation"""
        value_str = str(value).zfill(2)
        self.current_value = value_str
        self.next_value = value_str
        self.flip_progress = 0.0
        self.is_flipping = False
        self.flip_timer.stop()
        self.update()


class AnimatedFlipNumber(QLabel):
    """Keeping for compatibility"""
    pass
    
    def update_value(self, value):
        """Update the displayed value"""
        self.setText(str(value).zfill(2))


class FlipClock(QWidget):
    """Main flip clock widget combining hours, minutes, and seconds with animation"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        """Initialize UI components"""
        # Container for clock and date
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        
        # Clock layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Hours
        self.hours = FlipNumberWidget("12")
        layout.addWidget(self.hours)
        
        # Separator - colon with blinking
        separator1 = BlinkingSeparator()
        layout.addWidget(separator1)
        
        # Minutes
        self.minutes = FlipNumberWidget("38")
        layout.addWidget(self.minutes)
        
        # Separator - colon with blinking
        separator2 = BlinkingSeparator()
        layout.addWidget(separator2)
        
        # Seconds
        self.seconds = FlipNumberWidget("45")
        layout.addWidget(self.seconds)
        
        # AM/PM indicator - separate on the right
        ampm_layout = QVBoxLayout()
        ampm_layout.setContentsMargins(0, 0, 0, 0)
        ampm_layout.setSpacing(0)
        ampm_layout.addStretch()
        
        self.ampm = QLabel("AM")
        self.ampm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ampm_font = QFont()
        ampm_font.setPointSize(40)
        ampm_font.setBold(True)
        self.ampm.setFont(ampm_font)
        self.ampm.setStyleSheet("color: #4a7adb; margin-left: 2px; font-weight: bold;")
        
        ampm_layout.addWidget(self.ampm)
        ampm_layout.addStretch()
        layout.addLayout(ampm_layout)
        
        container_layout.addLayout(layout)
        
        # Date label
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("color: #666; font-size: 12px; margin-top: 10px;")
        container_layout.addWidget(self.date_label)
        
        # Set styling
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 12px;
                padding: 30px;
            }
        """)
    
    def setup_timer(self):
        """Setup timer to update clock every second"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()  # Initial update
    
    def update_time(self):
        """Update the displayed time"""
        now = datetime.now()
        
        # Update time components with animation
        hours = now.hour % 12 or 12
        minutes = now.minute
        seconds = now.second
        
        self.hours.animate_flip(hours)
        self.minutes.animate_flip(minutes)
        self.seconds.animate_flip(seconds)
        
        # Update AM/PM
        ampm = "PM" if now.hour >= 12 else "AM"
        self.ampm.setText(ampm)
        
        # Update date
        date_str = now.strftime("%A, %B %d")
        self.date_label.setText(date_str)
