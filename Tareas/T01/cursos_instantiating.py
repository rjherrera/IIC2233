

    M1 = Modulo(dia='M', modulo=1)
    J1 = Modulo(dia='J', modulo=1)
    M2 = Modulo(dia='M', modulo=2)
    J2 = Modulo(dia='J', modulo=2)
    W5 = Modulo(dia='W', modulo=5)
    W6 = Modulo(dia='W', modulo=6)
    H1 = Horario(tipo='Cátedra', sala='B13', modulos=[M1, J1])
    H2 = Horario(tipo='Ayudantía', sala='B13', modulos=[J2])
    H3 = Horario(tipo='Laboratorio', sala='B13', modulos=[W5, W6])

    C1 = Curso(nombre='Introducción a la Universidad',
               sigla='PUC0001',
               NRC=10012,
               retiro=True,
               ingles=False,
               seccion=1,
               aprobacion=False,
               profesor='Ignacio Sánchez',
               campus='San Joaquín',
               creditos=10,
               capacidad=100,
               horarios=[H1, H2, H3])

    C2 = Curso(nombre='Introducción a la Universidad',
               sigla='PUC0001',
               NRC=10013,
               retiro=True,
               ingles=False,
               seccion=2,
               aprobacion=False,
               profesor='Ignacio Sánchez',
               campus='San Joaquín',
               creditos=10,
               capacidad=100,
               horarios=[H1, H2, H3])

    print([M1, W6])
    print([H1, H3])
    print([C1, C2])
    print(M1)
    print(W6)
    print(H1)
    print(H2)
    print(C1)
    print(C2)
