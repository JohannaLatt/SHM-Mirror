from PyQt5 import QtCore
from PyQt5.QtCore import QEasingCurve, QVariant, QVariantAnimation
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel


class AnimationLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)

        # Invisible by default
        self.changeColor(QColor(255, 255, 255, 0))

        # Connect to fade-animation
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.changeColor)

    @QtCore.pyqtSlot(QVariant)
    def changeColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)

    def fadeIn(self, time=1):
        self.animation.stop()
        self.animation.setStartValue(self.palette().color(QPalette.WindowText))
        self.animation.setEndValue(QColor(255, 255, 255, 255))
        self.animation.setDuration(time)
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.start()

    def fadeOut(self, time=1):
        self.animation.stop()
        self.animation.setStartValue(self.palette().color(QPalette.WindowText))
        self.animation.setEndValue(QColor(255, 255, 255, 0))
        self.animation.setDuration(time)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()
