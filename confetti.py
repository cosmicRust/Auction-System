from PyQt6.QtWidgets import QDialog, QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QColor, QBrush
import random

class ConfettiWidget(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Player Sold!")
        self.setFixedSize(400, 300)
        
        # Layout
        layout = QVBoxLayout(self)
        self.message_label = QLabel(message)
        self.message_label.setObjectName("soldMessage")
        layout.addWidget(self.message_label)
        
        # Graphics view for confetti
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        
        # Confetti animation
        self.confetti = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_confetti)
        self.timer.start(50)
        
        # Create initial confetti
        for _ in range(50):
            x = random.randint(0, 400)
            y = random.randint(-300, 0)
            size = random.randint(5, 15)
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            rect = self.scene.addRect(x, y, size, size, brush=QBrush(color))
            self.confetti.append({"rect": rect, "vy": random.uniform(2, 5)})
    
    def update_confetti(self):
        for conf in self.confetti:
            rect = conf["rect"]
            pos = rect.rect()
            pos.moveTop(pos.top() + conf["vy"])
            if pos.top() > 300:
                pos.moveTop(-10)
                pos.moveLeft(random.randint(0, 400))
            rect.setRect(pos)
        
        self.scene.update()