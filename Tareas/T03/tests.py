from tablero import Tablero


class TestTablero:

    def setup_method(self, method):
        self.tablero = Tablero(15)

    def test_obtener_vehiculo(self):
        v = self.tablero.obtener_vehiculo('Lancha')  # vehiculo no None
        assert v is not None

    def test_obtener_vehiculo_letra(self):
        v = self.tablero.obtener_vehiculo_letra('C')  # vehiculo no None
        assert v is not None
