import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint

class DesktopWidget(QLabel):
    def __init__(self):
        super().__init__()

        # Load image
        pixmap = QPixmap("ascend.jpg")  # Replace with your image file
        self.setPixmap(pixmap)

        # Set window properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |  
                            Qt.WindowType.Tool)                 
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  

        # Close button
        self.close_btn = QPushButton("X", self)
        self.close_btn.setStyleSheet("background: red; color: white; border: none; font-weight: bold;")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.move(self.width() - 25, 5)
        self.close_btn.clicked.connect(self.quit_app)  # Proper close method

        # Move widget to a starting position
        self.move(100, 100)
        self.show()

    def mousePressEvent(self, event):
        """Capture initial mouse position when dragging starts"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Move the widget while dragging"""
        if hasattr(self, 'drag_position') and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()

    def quit_app(self):
        """Gracefully close the widget and exit the application"""
        self.close()  # Close the widget
        QApplication.quit()  # Ensure the whole app exits properly

# Run the application
app = QApplication(sys.argv)
widget = DesktopWidget()

# Move widget to the BACK of all windows
widget.lower()

sys.exit(app.exec())
