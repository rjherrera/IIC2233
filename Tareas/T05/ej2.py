# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore


class SpriteAnimation():

    def __init__(self, image_path, sprite_width, sprite_height, label):
        pixmap = QtGui.QPixmap(image_path)

        width, height = pixmap.width(), pixmap.height()
        self.pixmaps = []
        for x in range(0, width, sprite_width):
            for y in range(0, height, sprite_height):
                self.pixmaps.append(pixmap.copy(x, y,
                                                sprite_width, sprite_height))
        self._current_frame = 0
        self.label = label

    def play(self, interval=100):
        self._timer = QtCore.QTimer(interval=interval,
                                    timeout=self._animation_step)
        self._timer.start()

    def _animation_step(self):
        self.label.setPixmap(self.pixmaps[self._current_frame])
        self.label.update()
        self._current_frame += 1
        if self._current_frame >= len(self.pixmaps):
            self._current_frame = 0


class Window(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(100, 100)
        layout = QtGui.QVBoxLayout(self)
        label = QtGui.QLabel()
        layout.addWidget(label)
        # http://content.makeyourflashgame.com/pbe/tutorials/star-green.png
        self.animation = SpriteAnimation('zombie_0.png', 128, 128, label)
        self.animation.play()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
