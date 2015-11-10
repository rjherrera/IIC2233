from PyQt4 import QtGui, QtCore
_CORNER_DIR = {'L': 0, 'TL': 1, 'T': 2, 'TR': 3,
               'R': 4, 'BR': 5, 'B': 6, 'BL': 7}


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

    def movement(self, play_once=False):
        # pos = self.label.pos()
        # if displace:
        #     self.label.move(self.label.x() + 2, self.label.y() + 2)
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
        if hasattr(self, '_timer'):
            self._timer.stop()
        if hasattr(self, 'move_timer'):
            self.move_timer.stop()

    def start(self):
        if hasattr(self, '_timer'):
            self._timer.start()
        if hasattr(self, 'move_timer'):
            self.move_timer.start()


class CharacterSprite(Sprite):

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
        self.label.setPixmap(self.pixmaps[self.current_frame])
        self.is_dead = False

    @property
    def current_frame(self):
        return self._current_frame + self._direction + self._start_frame

    @property
    def place(self):
        xi = self.label.x()
        xf = xi + self.label.width()
        yi = self.label.y()
        yf = yi + self.label.height()
        return (range(xi + ((xf - xi) // 4), xf - ((xf - xi) // 4)),
                range(yi + ((yf - yi) // 4), yf - ((yf - yi) // 4)))

    def set_direction(self, corner):
        if corner in _CORNER_DIR:
            self._direction = _CORNER_DIR[corner]
        self.label.setPixmap(self.pixmaps[self.current_frame])

    def walk(self):
        self._start_frame, self._stop_frame = self.ranges['walk']
        self.movement()

    def attack(self):
        self._start_frame, self._stop_frame = self.ranges['attack']
        if hasattr(self, 'is_user'):
            self.movement(True)
        else:
            self.movement(False)

    def die(self):
        self._start_frame, self._stop_frame = self.ranges['die']
        # self._current_frame = 0
        self.movement(True)

    def stand(self):
        self._start_frame, self._stop_frame = 0, 0
        self.stay()

    def play(self, interval=100, fx='walk'):
        fx = self.movements[fx]
        self._timer = QtCore.QTimer(interval=interval,
                                    timeout=fx)
        self._timer.start()
