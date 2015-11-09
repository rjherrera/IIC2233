# -*- coding: utf-8 -*-
from PyQt4 import uic
# from time import sleep
from random import expovariate, randint  # choice
from datetime import timedelta
from sprites import *
from utils import *


form = uic.loadUiType("zombies.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        BG_TILE = 'sources/Wooden_Floor_Tile.gif'
        # TOP_TILE = 'sources/White_Stone_Tile.gif'
        css = 'QWidget#widget { background-image: url(%s); }' % BG_TILE
        self.widget.setStyleSheet(css)
        # css_main = ('QWidget#centralwidget { background-image: url(%s); }'
        #             % TOP_TILE)
        # self.centralwidget.setStyleSheet(css_main)

        # PLAYER
        self.labelPlayer.setScaledContents(True)
        self.labelPlayer.resize(_SPRITE_SIZE, _SPRITE_SIZE)
        self.center_label(self.labelPlayer)
        self.animation = CharacterSprite(_MAGE, 'skeleton_mage.png',
                                         256, 256, self.labelPlayer)
        # self.animation.play(interval=150, fx='walk')
        # PLAYER

        # TIEMPO DE JUEGO
        self.time_elapsed = timedelta(seconds=0)
        self.timer = QtCore.QTimer(interval=1000, timeout=self.time)
        self.timer.start()
        # TIEMPO DE JUEGO

        # APARICION DE ZOMBIES
        self.zombie_timer = QtCore.QTimer(interval=100,
                                          timeout=self.add_zombie)
        self.zombie_timer.start()
        self.labels = []
        self.animations = []
        for i in range(20):
            label = QtGui.QLabel('', self.widget)
            self.labels.append(label)
            label.move(1, 50)
            label.resize(50, 50)
        # APARICION DE ZOMBIES

        # BALAS
        self.bullets_labels = []
        for i in range(30):
            label = QtGui.QLabel('', self.widget)
            self.bullets_labels.append(label)
            label.move(1, 50)
            label.setScaledContents(True)
            label.resize(16, 16)
        self.bullets = []
        self.take_bullets_timer = QtCore.QTimer(interval=3000,
                                                timeout=self.take_bullets)
        # BALAS

        # COMIDA / AMMO
        self.care_packages_timer = QtCore.QTimer(interval=3000,
                                                 timeout=self.care_package)
        self.care_packages_timer.start()
        self.care_package_label = QtGui.QLabel('', self.widget)
        # COMIDA / AMMO

        # LIMPIEZA DE ZOMBIES
        self.cleaning_timer = QtCore.QTimer(interval=5000,
                                            timeout=self.clean_zombies)
        self.cleaning_timer.start()
        # LIMPIEZA DE ZOMBIES

        # POSICION DEL MOUSE
        self.widget.setMouseTracking(True)
        self.widget.mouseMoveEvent = self.mouseMoveEvent
        size = self.widget.geometry().size()
        self.mouse_pos = (size.width() // 2, size.height() // 2)
        # POSICION DEL MOUSE

        # BOTONES
        self.pushButtonPause.clicked.connect(self.pause)
        # self.pushButtonRestart.clicked.connect(self.add_zombie)
        self.pushButtonQuit.clicked.connect(self.stop_game)
        # BOTONES

        # SCORE
        self.score = 0
        self.ammo = 30
        self.max_ammo = 30
        self.ammo_picked = 0
        self.progressBarAmmo.setValue(self.ammo)
        self.progressBarAmmo.setMaximum(self.max_ammo)
        self.health = 100
        self.max_health = 100
        self.food_picked = 0
        self.progressBarHealth.setValue(self.health)
        self.progressBarHealth.setMaximum(self.max_health)
        self.zombies_added = 0
        self.zombies_killed = 0
        # SCORE

        # hacer que se siga el mouse para todos los childs?
        for child in self.findChildren(QtCore.QObject):
            try:
                child.setMouseTracking(True)
            except:
                pass

        # MOV
        self.accumulated = 0

    def center_label(self, label):
        size = self.widget.geometry().size()
        w, h = size.width(), size.height()
        label_size = label.size()
        w_l, h_l = label_size.width(), label_size.height()
        label.move(w // 2 - w_l // 2, h // 2 - h_l // 2)

    def update_score(self):
        self.labelScore.setText(str(self.score))

    def update_ammo(self, value):
        self.progressBarAmmo.setValue(self.ammo + value)
        self.ammo = self.progressBarAmmo.value()

    def time(self):
        self.time_elapsed += timedelta(seconds=1)
        self.labelTime.setText(str(self.time_elapsed)[2:7])
        if self.time_elapsed.seconds % 20 == 0:
            self.score += 5
            self.update_score()

    def move_animation(self, to_x, to_y):
        offset = (_SPRITE_SIZE // 3)
        half_off = _SPRITE_SIZE // 2
        if -offset < to_x < 500 + offset and -offset < to_y < 360 + offset:
            self.labelPlayer.move(to_x, to_y)
            xi = self.care_package_label.x()
            xf = xi + self.care_package_label.width()
            yi = self.care_package_label.y()
            yf = yi + self.care_package_label.height()
            # print(to_x + half_off, to_y + half_off, range(xi, xf), range(yi, yf))
            if (to_x + half_off in range(xi, xf) and
                    to_y + half_off in range(yi, yf)):
                self.take_care_package()
        if self.accumulated > _R:
            self.animation.walk()
            self.accumulated = 0

    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x() - self.labelPlayer.x()  # 260 = POS_PLAYER_X
        y = -(QMouseEvent.y() - self.labelPlayer.y())  # 150 = POS_PLAYER_Y
        direction = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, x, y)
        self.labelX.setText(str(x))
        self.labelY.setText(str(y))
        self.labelM.setText(str(direction))
        self.animation.set_direction(direction)
        self.mouse_pos = QMouseEvent.x(), QMouseEvent.y()

    def mousePressEvent(self, QMouseEvent):
        # create bullet thread (timer) and move it towards the objective
        # if at any time it is in the ranges (any animation.place)
        # do everything involved in elimination.
        if self.ammo <= 0:
            return
        self.update_ammo(-1)

        # ec de la recta:
        x1, y1 = QMouseEvent.x(), QMouseEvent.y() - 140
        off = self.labelPlayer.width() // 2
        x2, y2 = self.labelPlayer.x() + off, self.labelPlayer.y() + off

        if x2 > x1:
            m = (y2 - y1) / (x2 - x1)
            x1 -= 6000
            y1 = int(m * (x1 - x2) + y2)
        elif x2 < x1:
            m = (y2 - y1) / (x2 - x1)
            x1 += 6000
            y1 = int(m * (x1 - x2) + y2)
            print(x1, y1, x2, y2)
        elif y2 < y1:
            y1 += 2000
        elif y2 > y1:
            y1 -= 2000
        else:
            print(x1, y1, x2, y2)

        # MOVIMIENTO DE ATAQUE
        if hasattr(self.animation, '_timer'):
            self.animation._current_frame = 0
            del self.animation._timer
        self.animation.play(50, 'attack')
        # MOVIMIENTO DE ATAQUE

        # creando bala y definiendo trayectoria
        import functools
        from rect_eq import get_line
        bullet = QtCore.QTimer()
        points = get_line(x2, -y2, x1, -y1)
        # print(len(points))
        bullet.next_point = iter(points)
        bullet.label = self.bullets_labels.pop()
        # bullet.y = lambda x: int(m * (x - x1) + y1)
        pixmap = QtGui.QPixmap('sources/bullet_black.png')
        bullet.label.move(x2, y2)
        bullet.label.setPixmap(pixmap)
        callback = functools.partial(self.bullet_travel, bullet=bullet)
        bullet.timeout.connect(callback)
        bullet.start(2)
        self.bullets.append(bullet)
        # pasandole al callback la bala

        # POR AHORA SI SE HACE CLICK EN EL MONITO
        # click_x, click_y = QMouseEvent.x(), QMouseEvent.y() - 140
        # animation = None
        # for zombie in self.animations:
        #     ancho, largo = zombie.place
        #     if click_x in ancho and click_y in largo:
        #         animation = zombie
        # if animation is not None:
        #     self.zombies_killed += 1
        #     animation.is_dead = True
        #     label = animation.label
        #     del animation._timer
        #     animation.play(150, 'die')
        #     self.labels.insert(0, label)
        #     self.score += 1
        #     self.update_score()
        self.labelKilled.setText(str(self.zombies_killed))
        # animation.stop()
        # if algo, dícese "le achuntó al zombie"
        # del animation._timer
        # del animation

    def keyPressEvent(self, QKeyEvent):
        # mx, my = self.mouse_pos
        x, y = self.labelPlayer.x(), self.labelPlayer.y()
        # mrx, mry = mx - x, -(my - y)
        # direction = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, mrx, mry)
        # self.animation.set_direction(direction)
        dx, dy = _DIR_MOVEMENT[self.animation._direction]
        self.accumulated += _R
        if QKeyEvent.key() == QtCore.Qt.Key_W:
            self.move_animation(x + dx, y + dy)
        elif QKeyEvent.key() == QtCore.Qt.Key_S:
            self.move_animation(x - dx, y - dy)
        elif QKeyEvent.key() == QtCore.Qt.Key_A:
            self.move_animation(x + dy, y - dx)
        elif QKeyEvent.key() == QtCore.Qt.Key_D:
            self.move_animation(x - dy, y + dx)

    def pause(self):
        self.timer.stop()
        self.pushButtonPause.setText('►')
        self.pushButtonPause.clicked.connect(self.resume)
        self.widget.hide()

    def resume(self):
        self.timer.start()
        self.pushButtonPause.setText('။')
        self.pushButtonPause.clicked.connect(self.pause)
        self.widget.show()

    def tasa_zombies(self):
        # x(t) = 1/5 + 1/50t
        return (1 / 5) + (self.time_elapsed.seconds) / 50

    def add_zombie(self):
        self.zombies_added += 1
        if self.zombies_added > 4:
            return
        intervalo = round(expovariate(self.tasa_zombies()) + 0.5)
        self.zombie_timer.setInterval(intervalo * 1000)  # milisec to sec
        label = self.labels.pop()
        label.setScaledContents(True)
        label.resize(_SPRITE_SIZE, _SPRITE_SIZE)
        animation = CharacterSprite(_ZOMBIE, 'zombie_0.png',
                                    128, 128, label)
        # animation.set_direction('TL')
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

    def clean_zombies(self):
        for zombie in self.animations:
            if zombie.is_dead:
                zombie.label.clear()
                zombie.label.move(0, -50)
                zombie.stop()
                self.labels.append(zombie.label)
                del zombie._timer
        self.animations = [i for i in self.animations if not i.is_dead]

    def bullet_travel(self, bullet):
        x = bullet.label.x() + bullet.label.width() // 2
        y = bullet.label.y() + bullet.label.height() // 2
        try:
            to_x, to_y = next(bullet.next_point)
        except StopIteration:
            bullet.stop()
            return
        to_x, to_y = to_x, -to_y
        # print(to_x, to_y)
        bullet.label.move(to_x, to_y)
        animation = None
        if not (0 < to_x < 600 and 0 < to_y < 480):
            bullet.label.clear()
            bullet.label.move(0, -50)
            bullet.stop()
            self.bullets_labels.append(bullet.label)
            del bullet
            return
        for zombie in self.animations:
            ancho, largo = zombie.place
            if x in ancho and y in largo:
                animation = zombie
        if animation is not None:
            self.zombies_killed += 1
            animation.is_dead = True
            label = animation.label
            del animation._timer
            animation.play(150, 'die')
            self.labels.insert(0, label)
            self.score += 1
            self.update_score()
            bullet.label.clear()
            bullet.label.move(0, -50)
            bullet.stop()
            self.bullets_labels.append(bullet.label)
            del bullet
        self.labelKilled.setText(str(self.zombies_killed))

    def care_package(self):
        self.care_package_label.clear()
        self.care_package_label.move(0, -50)
        self.care_packages_timer.setInterval(randint(10, 30) * 1000)
        x = randint(0, 500)
        y = randint(0, 400)
        image_path = 'sources/Supply_Crate.gif'
        supply = 'health'
        amount = randint(10, 20)
        if randint(0, 1) != 0:
            image_path = 'sources/Marked_Crate.gif'
            supply = 'ammo'
            amount = randint(5, 10)
        self.care_package_label.supply = supply
        self.care_package_label.amount = amount
        pixmap = QtGui.QPixmap(image_path)
        self.care_package_label.setPixmap(pixmap)
        self.care_package_label.setScaledContents(True)
        self.care_package_label.resize(32, 32)
        self.care_package_label.move(x, y)

    def take_care_package(self):
        package = self.care_package_label
        package.clear()
        package.move(0, -50)
        if package.supply == 'ammo':
            self.ammo += package.amount
            if self.ammo + package.amount <= self.max_ammo:
                self.ammo += package.amount
            else:
                self.ammo = self.max_ammo
            self.ammo_picked += 1
            self.labelAmmo.setText(str(self.ammo_picked))
        elif package.supply == 'health':
            if self.health + package.amount <= self.max_health:
                self.health += package.amount
            else:
                self.health = self.max_health
            self.food_picked += 1
            self.labelFood.setText(str(self.food_picked))
        self.progressBarAmmo.setValue(self.ammo)
        self.progressBarHealth.setValue(self.health)

    def take_bullets(self):
        for bullet in self.bullets[:-2]:
            bullet.clear()
            self.bullets_labels.append(bullet)

    def stop_game(self):
        self.timer.stop()
        self.zombie_timer.stop()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
