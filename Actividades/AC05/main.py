# coding=utf-8

# Recuerda borrar los 'pass'. Pudes borrar si quieres los comentarios.


class Commit:

    id_actual = 0

    def __init__(self, message, changes):
        Commit.id_actual += 1
        self.id = Commit.id_actual
        self.message = message
        self.changes = changes
        self.commit_anterior = None
        self.commit_siguiente = None
        #############
        # COMPLETAR:
        # 'changes' es una lista de tuplas.
        # Puedes modificar esta clase a gusto tuyo.
        #############


class Branch:

    id_actual = 0

    def __init__(self, nombre, last_commit=None):
        Branch.id_actual += 1
        self.id = Branch.id_actual
        self.nombre = nombre
        self.last_commit = last_commit

    def new_commit(self, commit):
        commit.commit_anterior = self.last_commit
        if self.last_commit is not None:
            self.last_commit.commit_siguiente = commit
        self.last_commit = commit

    def pull(self):
        files = []
        temp = self.last_commit
        first = None
        while temp:
            ant = temp
            temp = temp.commit_anterior
            if temp is None:
                first = ant
        while first:
            for i, j in first.changes:
                files.append((i, j))
            first = first.commit_siguiente
        for action, f in files:
            if action == 'DELETE':
                indice = files.index((action, f))
                for i in files[:indice]:
                    if i[1] == f:
                        files.pop(files.index(i))
                        files.pop(files.index((action, f)))
        files = [i[1] for i in files]
        #############
        # COMPLETAR:
        # Retornar el estado final de esta branch (una lista de archivos).
        #############
        return files

    def get_final_state(self):
        files = []
        temp = self.last_commit
        first = None
        while temp:
            ant = temp
            temp = temp.commit_anterior
            if temp is None:
                first = ant
        while first:
            for i, j in first.changes:
                files.append((i, j))
            first = first.commit_siguiente
        for action, f in files:
            if action == 'DELETE':
                indice = files.index((action, f))
                for i in files[:indice]:
                    if i[1] == f:
                        files.pop(files.index(i))
                        files.pop(files.index((action, f)))
        return files


class Repository:

    def __init__(self, name):
        self.name = name
        b = Branch('master')
        c = Commit(message='commit inicial', changes=[('CREATE', '.jit')])
        b.new_commit(c)
        self.first_branch = b
        self.branches = [b]
        #############
        # COMPLETAR:
        # Crear branch 'master'.
        # Crear commit inicial y agregarlo a 'master'.
        #############

    def create_branch(self, new_branch_name, from_branch_name):
        #############
        # COMPLETAR:
        # Crear branch a partir del último estado de la 'from_branch_name'.
        #############
        b = Branch(new_branch_name)
        b_from = self.branch(from_branch_name)
        c = Commit(message=new_branch_name + ' initial',
                   changes=b_from.get_final_state())
        self.branches.append(b)
        return b

    def branch(self, branch_name):
        for i in self.branches:
            if i.nombre == branch_name:
                return i

    def checkout(self, commit_id):
        files = []
        for i in self.branches:
            temp = i.last_commit
            while temp:
                if temp.id == commit_id:
                    pass
                temp = temp.commit_anterior
        #############
        # COMPLETAR:
        # Buscar el commit con cierta id y retornar el estado del repositorio
        # hasta ese commit. Puede estar en cualquier branch.
        #############
        return files



b = Branch('Mi rama')
c = Commit(message="Borrar datos viejos y nuevas instrucciones",
           changes=[("CREATE", "data.txt"), ("CREATE", "README.md")])
b.new_commit(c)
c = Commit(message="Borrar datos viejos y nuevas instrucciones",
           changes=[("DELETE", "data.txt")])
b.new_commit(c)
c = Commit(message="Borrar datos viejos y nuevas instrucciones",
           changes=[("CREATE", "data.txt"), ("CREATE", "asasREADME.md")])
b.new_commit(c)
print(b.pull())
if __name__ == '__main__':
    # Ejemplo de uso
    # Puedes modificarlo para probar esto pero al momento de la corrección
    # el ayudante borrará cualquier cambio y restaurará las siguientes lineas
    # a su estado original (como se muestran aquí).

    repo = Repository("syllabus 2.0")

    repo.branch("master").new_commit(Commit(
        message="agregado readme",
        changes=[("CREATE", "README.md")]
    ))

    repo.branch("master").new_commit(Commit(
        message="archivos base",
        changes=[("CREATE", "main.py"), ("CREATE", "clases.py")]
    ))

    # Creamos una rama del estado actual de 'master'
    repo.create_branch("desarrollo-de-vistas", 'master')
    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="imagenes",
        changes=[("CREATE", "main.jpg"), ("CREATE", "user.png")]
    ))

    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="cambiar instrucciones",
        changes=[("DELETE", "README.md"), ("CREATE", "instrucciones.html")]
    ))

    repo.branch("master").new_commit(Commit(
        message="datos recolectados",
        changes=[("CREATE", "data.csv")]
    ))

    print(repo.branch("master").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'data.csv']

    print(repo.branch("desarrollo-de-vistas").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'main.py', 'clases.py',
    #  'main.jpg', 'user.png', 'instrucciones.html']

    print(repo.checkout(4))
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'main.jpg', 'user.png']

    print(repo.checkout(1))
    # Esperamos que el repo esté así:
    # ['.jit']
