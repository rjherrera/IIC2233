__all__ = ['_SPRITE_SIZE', '_MAGE', '_R', '_ZOMBIE',
           '_DIR_MOVEMENT', 'get_corner', 'get_line', 'opuesta']


_ZOMBIE = {'walk': (32, 89), 'attack': (96, 169), 'die': (176, 225)}
_MAGE = {'walk': (32, 89), 'attack': (96, 169), 'die': (176, 217)}
_SPRITE_SIZE = 100
_R = 3  # desplazamiento
_DIR_MOVEMENT = {0: (-_R, 0), 1: (-_R, -_R), 2: (0, -_R), 3: (_R, -_R),
                 4: (_R, 0), 5: (_R, _R), 6: (0, _R), 7: (-_R, _R)}


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


def opuesta(direccion):
    number_letter = {0: 'L', 1: 'TL', 2: 'T', 3: 'TR',
                     4: 'R', 5: 'BR', 6: 'B', 7: 'BL'}
    dicc = {'L': 4, 'TL': 5, 'T': 6, 'TR': 7,
            'R': 0, 'BR': 1, 'B': 2, 'BL': 3}
    return dicc[number_letter[direccion]]



# modified from
# http://stackoverflow.com/questions/25837544/get-all-points-of-a-straight-line-in-python
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    # print(points)
    return points
