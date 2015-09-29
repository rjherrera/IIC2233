import unittest
from main import Corrector
from os import listdir


class Tester(unittest.TestCase):

    def setUp(self):
        self.correcciones = []
        for n in listdir("Trabajos"):
            self.correcciones.append(Corrector(n))
        self.c1 = self.correcciones[0]
        self.c2 = self.correcciones[1]
        self.c3 = self.correcciones[2]
        self.c4 = self.correcciones[3]

    def test_revisar_nombre(self):
        self.assertTrue(self.c1.revisar_nombre())
        self.assertTrue(self.c2.revisar_nombre())
        self.assertFalse(self.c3.revisar_nombre())
        self.assertTrue(self.c4.revisar_nombre())

    def test_revisar_formato(self):
        self.assertTrue(self.c1.revisar_formato(self.c1.nombre.split('.')[-1]))
        self.assertTrue(self.c2.revisar_formato(self.c2.nombre.split('.')[-1]))
        self.assertTrue(self.c3.revisar_formato(self.c3.nombre.split('.')[-1]))
        self.assertFalse(self.c4.revisar_formato(self.c4.nombre.split('.')[-1]))
        # La función está mala, por lo que como no debería aceptar ttxtt entonces tira
        # un failure

    def test_revisar_verificador(self):
        self.assertTrue(self.c1.revisar_verificador(self.c1.nombre.split('_')[0]))
        self.assertTrue(self.c2.revisar_verificador(self.c2.nombre.split('_')[0]))
        self.assertFalse(self.c3.revisar_verificador(self.c3.nombre.split('_')[0]))
        self.assertTrue(self.c4.revisar_verificador(self.c4.nombre.split('_')[0]))

    def test_revisar_orden(self):
        self.assertTrue(self.c1.revisar_orden(self.c1.nombre.strip('.txt')))
        self.assertTrue(self.c2.revisar_orden(self.c2.nombre.strip('.txt')))
        self.assertTrue(self.c3.revisar_orden(self.c3.nombre.strip('.txt')))
        self.assertTrue(self.c4.revisar_orden(self.c4.nombre.strip('.ttxtt')))

    def test_get_palabras(self):
        self.assertEquals(self.c1.get_palabras(), 2262)
        self.assertEquals(self.c2.get_palabras(), 2262)
        self.assertEquals(self.c3.get_palabras(), 23)
        self.assertEquals(self.c4.get_palabras(), 23)
        # está malo el contador

    def test_get_descuento(self):
        self.assertEquals(self.c1.get_descuento(), 0)
        self.assertEquals(self.c2.get_descuento(), 0)
        self.assertEquals(self.c3.get_descuento(), 1.5)
        self.assertEquals(self.c4.get_descuento(), 1)

    def test_descontar(self):
        pass

    def tearDown(self):
        for n in listdir("Trabajos"):
            print(n)
            with open(n, 'w') as f:
                contenido = f.readlines()
                self.write('7.0\n')
                self.writelines(contenido)




suite = unittest.TestLoader().loadTestsFromTestCase(Tester)
unittest.TextTestRunner().run(suite)
