# -*- coding: utf-8 -*-
from PyQt4 import uic
# from time import sleep
from random import expovariate, randint  # choice
from datetime import timedelta
import functools
import pickle
import os
from sprites import *
from utils import *


form = uic.loadUiType("sources/zombies.ui")


class MainWindow(form[0], form[1]):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.best_score = 0
        self.load_score()

        self.widgetPause.hide()
        self.widgetEnd.hide()

        # estos son para los "boxes" redondeados que dejan que se vean textos
        # en la pantalla de bienvenida
        welcome_css = '''QLabel#labelWelcome { background-color : white;
                         border-radius: 5px; }'''
        self.labelWelcome.setStyleSheet(welcome_css)
        self.label_15.raise_()
        desc_css = '''QLabel#labelDesc { background-color : white;
                         border-radius: 3px; }'''
        self.labelDesc.setStyleSheet(desc_css)
        self.label_16.raise_()
        best_css = '''QLabel#labelScoreBg { background-color : white;
                         border-radius: 5px; }'''
        self.labelScoreBg.setStyleSheet(best_css)
        self.labelScoreBg.lower()
        self.label_18.raise_()
        self.labelBest.raise_()
        self.pushButtonPlay.clicked.connect(self.play)
        # fin de boxes

        # se definen BGs
        BG_TILE = 'sources/3.png'
        css = 'QWidget#widget { background-image: url(%s); }' % BG_TILE
        self.widget.setStyleSheet(css)
        BG_PS_TILE = 'sources/1.png'
        css = 'QWidget#widgetStart { background-image: url(%s); }' % BG_PS_TILE
        self.widgetStart.setStyleSheet(css)
        self.widgetStart.raise_()
        # fin BGS

        # PLAYER
        self.labelPlayer.setScaledContents(True)
        self.labelPlayer.resize(_SPRITE_SIZE, _SPRITE_SIZE)
        self.center_label(self.labelPlayer)
        self.animation = CharacterSprite(_MAGE, 'sources/skeleton_mage.png',
                                         256, 256, self.labelPlayer)
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
        self.care_packages_timer = QtCore.QTimer(interval=30000,
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
        self.pushButtonResumeBig.clicked.connect(self.resume)
        self.pushButtonQuit.clicked.connect(self.stop_game)
        self.pushButtonQuit_2.clicked.connect(self.quit_game)
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

        # hacer que se siga el mouse para todos los childs
        for child in self.findChildren(QtCore.QObject):
            try:
                child.setMouseTracking(True)
            except:
                pass

        # MOV
        self.accumulated = 0
        self.accumulated_fix = 0
        # Evita entre otros que algunas animaciones sean demasiado rápidas
        # o que persistan cuando no deben

        # INICIAR PAUSADO
        self.stop_timers()
        self.widget.hide()
        self.widgetStart.show()
        # INICIAR PAUSADO

    def play(self):
        self.widgetStart.hide()
        self.widget.show()
        self.start_timers()

    def stop_timers(self):
        # stopea todos los timers
        self.timer.stop()
        self.care_packages_timer.stop()
        self.zombie_timer.stop()
        self.cleaning_timer.stop()
        self.take_bullets_timer.stop()
        self.animation.stop()
        for animation in self.animations:
            animation.stop()
            if hasattr(animation, 'move_timer'):
                animation.move_timer.stop()

    def start_timers(self):
        # reinicia todos los timers
        self.timer.start()
        self.care_packages_timer.start()
        self.zombie_timer.start()
        self.cleaning_timer.start()
        self.take_bullets_timer.start()
        self.animation.start()
        for animation in self.animations:
            animation.start()
            if hasattr(animation, 'move_timer'):
                animation.move_timer.start()

    def center_label(self, label):
        # encuentra el centro de la app para poner ahí al
        # jugador al principio
        size = self.widget.geometry().size()
        w, h = size.width(), size.height()
        label_size = label.size()
        w_l, h_l = label_size.width(), label_size.height()
        label.move(w // 2 - w_l // 2, h // 2 - h_l // 2)

    def update_score(self):
        self.labelScore.setText(str(int(self.score)))

    def update_ammo(self, value):
        self.progressBarAmmo.setValue(self.ammo + value)
        self.ammo = self.progressBarAmmo.value()

    def update_health(self, value):
        self.progressBarHealth.setValue(self.health + value)
        self.health = self.progressBarHealth.value()
        if self.health <= 0:
            self.pushButtonQuit.click()

    def time(self):
        # se aumenta el tiempo y se muestra en el contador
        # ademas se aumenta el puntaje
        self.time_elapsed += timedelta(seconds=1)
        self.labelTime.setText(str(self.time_elapsed)[2:7])
        self.score += 0.25
        self.update_score()

    def move_animation(self, to_x, to_y):
        # se mueve al jugador hacia una posicion
        # y se ve si hay un care package, para tomarlo
        x = self.animation.label.x() + self.animation.label.width() // 2
        y = self.animation.label.y() + self.animation.label.height() // 2
        offset = (_SPRITE_SIZE // 3)
        half_off = _SPRITE_SIZE // 2
        if -offset < to_x < 500 + offset and -offset < to_y < 360 + offset:
            for z in self.animations:
                anch, larg = z.place
                if (x in anch and y in larg and
                        opuesta(self.animation._direction) == z._direction):
                    return
            self.labelPlayer.move(to_x, to_y)
            xi = self.care_package_label.x()
            xf = xi + self.care_package_label.width()
            yi = self.care_package_label.y()
            yf = yi + self.care_package_label.height()
            if (to_x + half_off in range(xi, xf) and
                    to_y + half_off in range(yi, yf)):
                self.take_care_package()
        if self.accumulated > _R:
            self.animation.walk()
            self.accumulated = 0

    def mouseMoveEvent(self, QMouseEvent):
        # se sigue el mouse y antes se mostraban las coordenadas
        # en pantalla pero se comentó para sacar eso
        x = QMouseEvent.x() - self.labelPlayer.x()  # 260 = POS_PLAYER_X
        y = -(QMouseEvent.y() - self.labelPlayer.y())  # 150 = POS_PLAYER_Y
        direction = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, x, y)
        # self.labelX.setText(str(x))
        # self.labelY.setText(str(y))
        # self.labelM.setText(str(direction))
        self.animation.set_direction(direction)
        self.mouse_pos = QMouseEvent.x(), QMouseEvent.y()

    def mousePressEvent(self, QMouseEvent):
        # create bullet thread (timer) and move it towards the objective
        # if at any time it is in the ranges (any animation.place)
        # do everything involved in elimination.
        if self.ammo <= 0:
            return
        self.update_ammo(-1)

        # obtengo los puntos sobre los que construire mi recta
        # y los extiendo para que alcancen a salir de la pantalla
        # sin embargo se considera que después como las balas no tienen
        # alcance infinito, se borran, con otro timer encagado de eso
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
            # print(x1, y1, x2, y2)
        elif y2 < y1:
            y1 += 2000
        elif y2 > y1:
            y1 -= 2000

        # MOVIMIENTO DE ATAQUE
        if hasattr(self.animation, '_timer'):
            self.animation._current_frame = 0
            del self.animation._timer
        self.animation.is_user = True
        self.animation.play(50, 'attack')
        # MOVIMIENTO DE ATAQUE

        # creando bala y definiendo trayectoria
        bullet = QtCore.QTimer()
        points = get_line(x2, -y2, x1, -y1)
        bullet.next_point = iter(points)
        bullet.label = self.bullets_labels.pop()
        pixmap = QtGui.QPixmap('sources/bullet_black.png')
        bullet.label.move(x2, y2)
        bullet.label.setPixmap(pixmap)
        callback = functools.partial(self.bullet_travel, bullet=bullet)
        bullet.timeout.connect(callback)
        bullet.start(2)
        self.bullets.append(bullet)
        # pasandole al callback la bala
        # por medio de partial de functools para poder usarlo
        # dentro del callback
        self.labelKilled.setText(str(self.zombies_killed))

    def keyPressEvent(self, QKeyEvent):
        x, y = self.labelPlayer.x(), self.labelPlayer.y()

        # Lo comentado abajo haría que el movimiento cambiara acorde se va
        # moviendo el jugador, interfiere en el juego, por eso se comenta

        # mx, my = self.mouse_pos
        # mrx, mry = mx - x, -(my - y)
        # direction = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, mrx, mry)
        # self.animation.set_direction(direction)

        # fin de ese detalle

        dx, dy = _DIR_MOVEMENT[self.animation._direction]
        self.accumulated += _R

        # PREVENT ANIMATION KEEP PLAYING AFTER SHOOTING
        self.accumulated_fix += _R
        if self.accumulated_fix > 13 * _R:
            self.animation.stop()
            self.accumulated_fix = 0
        # END PREVENTION

        if QKeyEvent.key() == QtCore.Qt.Key_W:
            self.move_animation(x + dx, y + dy)
        elif QKeyEvent.key() == QtCore.Qt.Key_S:
            self.move_animation(x - dx, y - dy)
        elif QKeyEvent.key() == QtCore.Qt.Key_A:
            self.move_animation(x + dy, y - dx)
        elif QKeyEvent.key() == QtCore.Qt.Key_D:
            self.move_animation(x - dy, y + dx)
        elif QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.pushButtonPause.click()

    def pause(self):
        self.stop_timers()
        self.pushButtonPause.setText('►')
        self.pushButtonPause.clicked.connect(self.resume)
        self.widget.hide()
        self.widgetPause.show()

    def resume(self):
        self.start_timers()
        self.pushButtonPause.setText('။')
        self.pushButtonPause.clicked.connect(self.pause)
        self.widgetPause.hide()
        self.widget.show()

    def tasa_zombies(self):
        # x(t) = 1/5 + 1/25t
        return (1 / 5) + (self.time_elapsed.seconds) / 25

    def add_zombie(self):
        self.zombies_added += 1
        # if self.zombies_added > 4:
        #     return
        intervalo = round(expovariate(self.tasa_zombies()) + 0.5)
        self.zombie_timer.setInterval(intervalo * 1000)  # milisec to sec
        label = self.labels.pop()
        label.setScaledContents(True)
        label.resize(_SPRITE_SIZE, _SPRITE_SIZE)
        animation = CharacterSprite(_ZOMBIE, 'sources/zombie_0.png',
                                    128, 128, label)
        animation.attacking = False
        animation.accumulated_attack = 0
        # posicionar los nuevos zombies en el borde
        rand = randint(0, 3)
        if rand == 0:
            pos = randint(-40, 530), -40
        elif rand == 1:
            pos = -40, randint(-40, 400)
        elif rand == 2:
            pos = 530, randint(-40, 400)
        else:
            pos = randint(-40, 530), 400
        # end posicionar

        label.move(*pos)
        animation.play(interval=150, fx='walk')
        animation.move_timer = QtCore.QTimer()
        self.animations.append(animation)
        callback = functools.partial(self.move_zombie, zombie=animation)
        animation.move_timer.timeout.connect(callback)
        animation.move_timer.start(20)
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

    def move_zombie(self, zombie):
        if zombie.is_dead:
            return
        x = zombie.label.x() + zombie.label.width() // 2
        y = zombie.label.y() + zombie.label.height() // 2
        x1, y1 = zombie.label.x(), zombie.label.y()
        x2, y2 = self.labelPlayer.x(), self.labelPlayer.y()
        xd = x2 - x1  # 260 = POS_PLAYER_X
        yd = -(y2 - y1)
        # cambio la direccion dinamicamente de acuerdo persigo al jugador
        corner = get_corner(_SPRITE_SIZE, _SPRITE_SIZE, xd, yd)
        zombie.set_direction(corner)
        points_zombie = get_line(x1, -y1, x2, -y2)
        to_x, to_y = points_zombie[1]
        to_x, to_y = to_x, -to_y
        ancho, largo = self.animation.place
        # se ve si hay otro zombie en el lugar y retorno (me quedo quieto)
        # si esque lo hay
        for other_z in self.animations:
            anch, larg = other_z.place
            if x in anch and y in larg and other_z != zombie:
                return
        if x in ancho and y in largo:
            if not zombie.attacking:
                # pongo la animacion de atacar si lo encuentro
                zombie._timer.stop()
                del zombie._timer
                zombie.play(150, 'attack')
                zombie.attacking = True
            if zombie.accumulated_attack > 20:
                self.update_health(-20)
                zombie.accumulated_attack = 0
            zombie.accumulated_attack += 1
        else:
            if zombie.attacking:
                zombie._timer.stop()
                del zombie._timer
                zombie.play(150, 'walk')
                zombie.attacking = False
            zombie.label.move(to_x, to_y)

    def bullet_travel(self, bullet):
        x = bullet.label.x() + bullet.label.width() // 2
        y = bullet.label.y() + bullet.label.height() // 2
        try:
            to_x, to_y = next(bullet.next_point)
        except StopIteration:
            bullet.stop()
            return
        to_x, to_y = to_x, -to_y
        # muevo la bala y si encuentro algo desaparezco y ataco
        bullet.label.move(to_x, to_y)
        animation = None
        # aqui me elimino si salí de la pantalla
        if not (0 < to_x < 600 and 0 < to_y < 480):
            bullet.label.clear()
            bullet.label.move(0, -50)
            bullet.stop()
            self.bullets_labels.append(bullet.label)
            del bullet
            return
        # aqui es donde busco si hay un zombie al q le achunte
        living_animations = [i for i in self.animations if not i.is_dead]
        for zombie in living_animations:
            ancho, largo = zombie.place
            if x in ancho and y in largo:
                animation = zombie
        # si habia procedo a realizar lo q corresponda
        # es decir liminar el zombie, sumar puntaje, etc
        if animation is not None:
            self.zombies_killed += 1
            animation.is_dead = True
            animation.label.lower()
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
            bullet.label.clear()
            self.bullets_labels.append(bullet.label)

    def save_score(self, score):
        if self.best_score < score:
            with open('sources/best_score.zombies', 'wb') as f:
                pickle.dump(score, f)

    def load_score(self):
        if 'best_score.zombies' in os.listdir('sources'):
            with open('sources/best_score.zombies', 'rb') as f:
                score = pickle.load(f)
                self.best_score = score
                self.labelBest.setText(str(int(score)))

    def stop_game(self):
        self.stop_timers()
        self.widget.hide()
        self.widgetEnd.show()
        self.labelScoreEnd.setText(str(int(self.score)))
        self.save_score(int(self.score))

    def quit_game(self):
        self.app.quit()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow(app)
    form.show()
    app.exec_()
