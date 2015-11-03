# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic
# from time import sleep
# from random import randint, choice
from datetime import datetime, timedelta


def get_corner(height, width, x, y):
    if x > width:
        if y > 0:
            return 'TR'
        elif y < -height:
            return 'BR'
        else:
            return 'R'
    elif x < 0:
        if y > 0:
            return 'TL'
        elif y < -height:
            return 'BL'
        else:
            return 'L'
    else:
        if y > 0:
            return 'T'
        elif y < -height:
            return 'B'
        else:
            return 'C'


class Sprite:

    def __init__(self, image_path, sprite_width, sprite_height, label):
        pixmap = QtGui.QPixmap(image_path)
        width, height = pixmap.width(), pixmap.height()
        self.pixmaps = []
        for x in range(0, width, sprite_width):
            for y in range(0, height, sprite_height):
                spr = pixmap.copy(x, y, sprite_width, sprite_height)
                self.pixmaps.append(spr)
        self._current_frame = 0
        self.label = label
        self.to = 0

    @property
    def current_frame(self):
        return self._current_frame

    # def move(self):
    #     self.label.setPixmap(self.pixmaps[self.current_frame])
    #     self.label.update()
    #     self._current_frame += 8
    #     if self.current_frame >= len(self.pixmaps):
    #         self._current_frame = 0

    def movement(self):
        # pos = self.label.pos()
        # self.label.move(pos.x() + 2, pos.y() + 2)
        self.label.setPixmap(self.pixmaps[self.current_frame])
        # self.label.update()
        self._current_frame += 8
        if self.current_frame >= self._stop_frame:
            self._current_frame = 0


class ZombieSprite(Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movements = {'walk': self.walk,
                          'attack': self.attack,
                          'die': self.die}
        self._start_frame = 0
        self._stop_frame = len(self.pixmaps) - 1
        self._direction = 5
        # self.states = {'normal': self.pixmaps[:8],
        #                'attacking': self.pixmaps[32:40]}
        # self._current_set = self.states['attacking']

    @property
    def current_frame(self):
        return self._current_frame + self._direction + self._start_frame

    def walk(self):
        self._start_frame = 32
        self._stop_frame = 89
        self.movement()

    def attack(self):
        self._start_frame = 96
        self._stop_frame = 169
        self.movement()

    def die(self):
        self._start_frame = 176
        self._stop_frame = 217
        self.movement()

    def play(self, interval=100, fx='walk'):
        fx = self.movements[fx]
        self._timer = QtCore.QTimer(interval=interval,
                                    timeout=fx)
        self._timer.start()


form = uic.loadUiType("zombies.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # PLAYER
        self.labelPlayer.setScaledContents(True)
        self.labelPlayer.resize(50, 50)
        self.animation = ZombieSprite(
            'zombie_topdown.png', 128, 128, self.labelPlayer)
        self.animation.play(interval=150, fx='walk')
        # PLAYER

        # TIEMPO DE JUEGO
        self.time_elapsed = timedelta(seconds=0)
        self.timer = QtCore.QTimer(interval=1000, timeout=self.time)
        self.timer.start()
        # TIEMPO DE JUEGO

        # POSICION DEL MOUSE
        # self.setMouseTracking(True)
        # self.frame.setMouseTracking(True)
        # self.frame.mouseMoveEvent = self.mouseMoveEvent
        self.widget.setMouseTracking(True)
        self.widget.mouseMoveEvent = self.mouseMoveEvent
        # POSICION DEL MOUSE

        # BOTONES
        self.pushButtonPause.clicked.connect(self.pause)
        self.pushButtonRestart.clicked.connect(self.add_zombie)
        self.n = 0

        # hacer que se siga el mouse para todos los childs?
        for child in self.findChildren(QtCore.QObject):
            try:
                child.setMouseTracking(True)
            except:
                pass

    def time(self):
        self.time_elapsed += timedelta(seconds=1)
        self.labelTime.setText(str(self.time_elapsed)[2:7])

    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x() - self.labelPlayer.x()  # 260 = POS_PLAYER_X
        y = -(QMouseEvent.y() - self.labelPlayer.y())  # 150 = POS_PLAYER_Y
        m = get_corner(50, 50, x, y)
        self.labelX.setText(str(x))
        self.labelY.setText(str(y))
        self.labelM.setText(str(m))

    def pause(self):
        # cuando se aprete pause se va a cambiar el movimiento a attack
        # self.animation._timer.timeout.connect(
        #     self.animation.movements['attack'])
        # y también se va a pausar o algo así
        self.timer.stop()
        self.animation._timer.stop()
        self.pushButtonPause.setText('►')
        self.pushButtonPause.clicked.connect(self.resume)

    def resume(self):
        self.timer.start()
        self.animation._timer.start()
        self.pushButtonPause.setText('။')
        self.pushButtonPause.clicked.connect(self.pause)

    def add_zombie(self):
        self.n += 1
        label = QtGui.QLabel('', self.widget)
        label.resize(50, 50)
        self.layout().addWidget(label)
        animation = ZombieSprite(
            'zombie_topdown.png', 128, 128, label)
        label.setScaledContents(True)
        label.move(0, 200)
        animation.play()
        self.show()
        # setattr(self, 'label%d' % self.n, label)
        # setattr(self, 'animation%d' % self.n, ZombieSprite(
        #     'zombie_topdown.png', 128, 128, label))


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
