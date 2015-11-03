# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic
# from time import sleep
from random import expovariate, randint  # choice
from datetime import timedelta

_ZOMBIE = {'walk': (32, 89), 'attack': (96, 169), 'die': (176, 225)}
_MAGE = {'walk': (32, 89), 'attack': (96, 169), 'die': (176, 217)}
_SPRITE_SIZE = 100


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

    def movement(self, displace=False, play_once=False):
        # pos = self.label.pos()
        if displace:
            self.label.move(self.label.x() + 2, self.label.y() + 2)
        self.label.setPixmap(self.pixmaps[self.current_frame])
        self._current_frame += 8
        if self.current_frame >= self._stop_frame:
            if play_once:
                self._current_frame -= 8
                self._timer.stop()
            else:
                self._current_frame = 0

    def stay(self):
        self.label.setPixmap(self.pixmaps[self.current_frame])

    def stop(self):
        self._timer.stop()


class CharacterSprite(Sprite):

    CORNER_DIR = {'L': 0, 'TL': 1, 'T': 2, 'TR': 3,
                  'R': 4, 'BR': 5, 'B': 6, 'BL': 7}

    def __init__(self, ranges, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movements = {'walk': self.walk,
                          'attack': self.attack,
                          'die': self.die,
                          'stand': self.stand}
        self.ranges = ranges
        self._start_frame = 0
        self._stop_frame = len(self.pixmaps) - 1
        self._direction = 5

    @property
    def current_frame(self):
        return self._current_frame + self._direction + self._start_frame

    def set_direction(self, corner):
        if corner in self.CORNER_DIR:
            self._direction = self.CORNER_DIR[corner]

    def walk(self):
        self._start_frame, self._stop_frame = self.ranges['walk']
        self.movement()

    def attack(self):
        self._start_frame, self._stop_frame = self.ranges['attack']
        self.movement()

    def die(self):
        self._start_frame, self._stop_frame = self.ranges['die']
        self.movement(True, True)

    def stand(self):
        self._start_frame, self._stop_frame = 0, 0
        self.stay()

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
        self.labelPlayer.resize(_SPRITE_SIZE, _SPRITE_SIZE)
        self.center_label(self.labelPlayer)
        self.animation = CharacterSprite(_MAGE, 'skeleton_mage.png',
                                         256, 256, self.labelPlayer)
        self.animation.play(interval=150, fx='walk')
        # PLAYER

        # TIEMPO DE JUEGO
        self.time_elapsed = timedelta(seconds=0)
        self.timer = QtCore.QTimer(interval=1000, timeout=self.time)
        self.timer.start()
        # TIEMPO DE JUEGO

        # APARICION DE ZOMBIES
        self.zombie_timer = QtCore.QTimer(interval=3000,
                                          timeout=self.add_zombie)
        self.zombie_timer.start()
        self.labels = []
        self.animations = []
        for i in range(50):
            label = QtGui.QLabel('', self.widget)
            self.labels.append(label)
            label.move(1, 50)
            label.resize(50, 50)
        # APARICION DE ZOMBIES

        # POSICION DEL MOUSE
        self.widget.setMouseTracking(True)
        self.widget.mouseMoveEvent = self.mouseMoveEvent
        # POSICION DEL MOUSE

        # BOTONES
        self.pushButtonPause.clicked.connect(self.pause)
        # self.pushButtonRestart.clicked.connect(self.add_zombie)
        self.pushButtonQuit.clicked.connect(self.stop_game)
        self.zombies_added = 0
        # BOTONES

        # SCORE
        self.score = 0
        # SCORE

        # hacer que se siga el mouse para todos los childs?
        for child in self.findChildren(QtCore.QObject):
            try:
                child.setMouseTracking(True)
            except:
                pass

    def center_label(self, label):
        size = self.widget.geometry().size()
        w, h = size.width(), size.height()
        label_size = label.size()
        w_l, h_l = label_size.width(), label_size.height()
        label.move(w // 2 - w_l // 2, h // 2 - h_l // 2)

    def update_score(self):
        self.labelScore.setText(str(self.score))

    def time(self):
        self.time_elapsed += timedelta(seconds=1)
        self.labelTime.setText(str(self.time_elapsed)[2:7])
        if self.time_elapsed.seconds % 20 == 0:
            self.score += 10
            self.update_score()

    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x() - self.labelPlayer.x()  # 260 = POS_PLAYER_X
        y = -(QMouseEvent.y() - self.labelPlayer.y())  # 150 = POS_PLAYER_Y
        m = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, x, y)
        self.labelX.setText(str(x))
        self.labelY.setText(str(y))
        self.labelM.setText(str(m))
        self.animation.set_direction(m)

    def mousePressEvent(self, QMouseEvent):
        animation = self.animations.pop()
        label = animation.label
        label.move(0, -50)
        label.clear()
        animation._timer.stop()
        self.labels.append(label)
        # if algo, dícese "le achuntó al zombie"
        # self.score += 1
        # self.update_score()
        del animation._timer
        del animation

    def pause(self):
        self.timer.stop()
        self.animation._timer.stop()
        self.pushButtonPause.setText('►')
        self.pushButtonPause.clicked.connect(self.resume)

    def resume(self):
        self.timer.start()
        self.animation._timer.start()
        self.pushButtonPause.setText('။')
        self.pushButtonPause.clicked.connect(self.pause)

    def tasa_zombies(self):
        # x(t) = 1/5 + 1/25t
        return (1 / 5) + (self.time_elapsed.seconds) / 50

    def add_zombie(self):
        self.zombies_added += 1
        # self.labelKilled.setText(str(self.zombies_added))
        intervalo = round(expovariate(self.tasa_zombies()) + 0.5)
        self.zombie_timer.setInterval(intervalo * 1000)  # milisec to sec
        label = self.labels.pop()
        label.setScaledContents(True)
        label.resize(110, 110)
        animation = CharacterSprite(_ZOMBIE, 'zombie_0.png',
                                    128, 128, label)
        # posicionar los nuevos zombies en el top left
        if randint(0, 1) == 1:
            pos = randint(0, 250), -30
        else:
            pos = 0, randint(0, 150)
        # end posicionar

        label.move(*pos)
        # label.setStyleSheet("border: 2px solid #222222")
        animation.play(interval=150, fx='walk')
        self.animations.append(animation)
        # self.zombie_timer.stop()

    def stop_game(self):
        self.animation.stop()
        self.timer.stop()
        self.zombie_timer.stop()
        for animation in self.animations:
            animation.stop()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
