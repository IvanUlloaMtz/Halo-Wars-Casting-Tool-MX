from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QRadialGradient, QColor
import math
import random

class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0.0
        self.blobs = []
        for _ in range(3): # 3 liquid blobs
            self.blobs.append({
                'phase': random.uniform(0, 2*math.pi),
                'speed': random.uniform(0.3, 0.7),
                'radius_factor': random.uniform(0.6, 1.2),
                'color_hue': random.uniform(0.6, 0.7) # Blue-ish hues
            })
            
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16) # ~60 FPS for extra smoothness
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def update_animation(self):
        self.angle += 0.01
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Base solid color (dark deep void)
        painter.fillRect(self.rect(), QColor(20, 20, 32))

        # Draw animated blobs
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Plus)
        for i, blob in enumerate(self.blobs):
            # Calculate blob position with complex oscillation
            px = self.width() * (0.5 + 0.4 * math.sin(self.angle * blob['speed'] + blob['phase']))
            py = self.height() * (0.5 + 0.4 * math.cos(self.angle * blob['speed'] * 0.7 + blob['phase'] * 1.3))
            
            radius = (self.width() + self.height()) / 2 * blob['radius_factor']
            
            # Subtle color pulse
            pulse = (math.sin(self.angle * 0.5 + i) + 1) / 2
            color = QColor.fromHslF(blob['color_hue'], 0.6, 0.2 + 0.1 * pulse, 0.4) # Semi-transparent
            
            grad = QRadialGradient(QPointF(px, py), radius)
            grad.setColorAt(0, color)
            grad.setColorAt(1, QColor(0, 0, 0, 0)) # Fades to fully transparent
            
            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.rect())
