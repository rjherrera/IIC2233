PESOS = {'madera': 10, 'ladrillos': 7, 'hormigon': 4, 'metal': 2}


class Casa:

    def __init__(self, material, rango):
        self.material = material
        self.rango = rango
        self.peso = PESOS[material]

    def __repr__(self):
        return ' ■'  # ⌂


class Hospital:

    pass


class Cuartel:

    pass


class Comisaria:

    pass
