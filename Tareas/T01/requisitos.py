# coding=utf-8


def final(ramos, logico, requisito):
    '''
    Entrega si cumple los requisitos de un string de la forma
    "RAMOoRAMOoRAMO" o "RAMOyRAMOyRAMO" o "RAMO", etc de modo
    que sirve como condicion final para la funcion recursiva
    "cumple"
    :param ramos: Lista de ramos aprobados por el alumno
    :param logico: Operador logico ya sea "y" u "o"
    :param requisito: String indicando los requisitos de un ramo
    :return: Boolean indicando si el requisito se cumple
    '''
    if logico == 'o':
        return bool(set(requisito).intersection(set(ramos)))
    elif logico == 'y':
        return set(requisito).issubset(set(ramos))
    return requisito in ramos


def posicion_corte(string):
    '''
    Entrega la posicion donde se debe cortar en derecha/izquierda
    el string, de modo de luego evaluar por separado ambos lados.
    Primero ve si no tiene parentesis innecesarios (por ejemplo
    "(ICM1231 o (ICM1231 y ICM1234))" donde sobran los de los extremos),
    y sino busca el primer parentesis que cierre.
    :param string: String conteniendo parentesis
    :return: Integer indicando posicion de corte adecuada
    '''
    if string[0] != '(':
        o = string.find('o')
        y = string.find('y')
        return min(o, y) if min(o, y) != -1 else max(o, y)
    while True:
        pos = string.find(')')
        if string[:pos].count('(') < 2:
            break
        string = string.replace('(', '|', 1).replace(')', '|', 1)
    return pos + 1


def cumple(ramos, requisito):
    '''
    Entrega el resultado de evaluar un string de requisitos contra
    una lista de ramos
    :param ramos: Lista de ramos aprobados por el alumno
    :param requisito: String indicando los requisitos de un ramo
    :return: Boolean indicando si cumple los requisitos
    '''
    if '(' not in requisito and ')' not in requisito:
        if 'o' in requisito:
            req = requisito.split('o')
            return final(ramos, 'o', req)
        elif 'y' in requisito:
            req = requisito.split('y')
            return final(ramos, 'y', req)
        return final(ramos, '-', requisito)
    pos = posicion_corte(requisito)
    if len(requisito) == pos:
        requisito = requisito[1:-1]
        pos = posicion_corte(requisito)
    izquierda = requisito[:pos]
    derecha = requisito[pos + 1:]
    logico = requisito[pos]
    if logico == 'o':
        return cumple(ramos, izquierda) or cumple(ramos, derecha)
    elif logico == 'y':
        return cumple(ramos, izquierda) and cumple(ramos, derecha)
    return False
