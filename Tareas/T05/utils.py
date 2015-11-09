__all__ = ['_SPRITE_SIZE', '_MAGE', '_R', '_ZOMBIE',
           '_DIR_MOVEMENT', 'get_corner']


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
