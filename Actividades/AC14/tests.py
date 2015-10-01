from main import Base, Alumno, Ramo


class TestSistema:

    def setup_method(self, method):
        self.base = Base()
        self.alumno = Alumno(base=self.base, creditos=0, nombre='Yo')
        self.base.db.append(Ramo('IIC2233A', '0', '0'))

    def test_inscribir_con_vacantes(self):
        ramo = self.base.db[0]  # ramo con vacantes
        assert self.base.inscribir(ramo.sigla, self.alumno)

    def test_inscribir_sin_vacantes(self):
        ramo = self.base.db[-1]  # ramo sin vacantes agregado antes
        assert not self.base.inscribir(ramo.sigla, self.alumno)

    def test_botar_vacantes(self):
        ramo = self.base.db[0]
        vacantes = ramo.vacantes  # vacantes antes de inscribir
        self.base.inscribir(ramo.sigla, self.alumno)  # deberia bajar en 1 las vacantes
        self.base.botar(ramo.sigla, self.alumno)  # deberia volver a subir las vacantes
        assert ramo.vacantes == vacantes  # revisar vacantes antes = vacantes despues

    def test_botar_creditos_lista(self):
        ramo = self.base.db[0]
        creditos = self.alumno.creditos_actuales  # creditos antes de inscribir
        self.alumno.tomar_ramo(ramo.sigla)  # inscribo deben subir los cred
        # y debe agregarse a la lista de ramos
        self.alumno.botar_ramo(ramo.sigla)  # boto debe vaciarse la lista y los cred bajar
        assert self.alumno.creditos_actuales == creditos and ramo.sigla not in self.alumno.ramos

    def test_revisar_repeticion(self):
        ramo = self.base.db[0]
        self.alumno.tomar_ramo(ramo.sigla)
        assert not self.alumno.tomar_ramo(ramo.sigla)

    def test_revisar_no_repeticion(self):
        ramo = self.base.db[0]
        ramo2 = self.base.db[1]
        self.alumno.tomar_ramo(ramo.sigla)
        assert not self.alumno.tomar_ramo(ramo2.sigla)

    def test_creditos_maximos_excedidos(self):
        assert not self.alumno.tomar_ramo('IIC2233')

    def test_creditos_maximos_no_excedidos(self):
        ramo = self.base.db[0]
        assert self.alumno.tomar_ramo(ramo.sigla)
