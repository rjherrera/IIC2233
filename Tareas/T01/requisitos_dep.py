ramos_alumno = ['MAT1620', 'FIS1513', 'MAT1610', 'ICM2313']
req1 = ('MAT1630(c) o MAT1523(c) o (FIS1512 y ING1011 y MAT1512) ' +
        'o (FIS1512 y IPP1000 y MAT1512) o (ICE1013 y ING1011 y MAT1512) ' +
        'o (ICE1013 y IPP1000 y MAT1512) o (FIS1522 y ING1011 y QIM100) o' +
        ' (FIS1522 y IPP1000 y QIM100)')
req2 = ('(FIS1513 y ICM2313) ' +
        'o (ICE1513 y ICM2313) ' +
        'o (FIS1513 y ICM2022) ' +
        'o (ICE1513 y ICM2022) ' +
        'o (IPP1000 y MAT1102 y MAT1503) ' +
        'o (ING1011 y MAT1102 y MAT1503) ' +
        'o (FIZ0121 y ICM2313) ' +
        'o (FIZ0121 y ICM2022) ' +
        'o (FIS1513 y ICM2313) ' +
        'o (ICE1513 y ICM2313) ' +
        'o (FIS1513 y ICM2022)')
req3 = '(ICM2303 o ICE2313 o ICM2028) y (ICM2313 o (ICE1302 y ICM1122 y ING1011) o (ICE1302 y ICM1122 y IPP1000))'
ramos_por_tomar = ['MAT1630']
ram = ['ICM2303', 'ICM2313', 'FIS1513']


def final(ramos, logico, requisito):
    print()
    print(ramos, 'debe contener alguno:' if logico == 'o' else 'debe contener todos:', requisito)
    if logico == 'o':
        print(bool(set(requisito).intersection(set(ramos))))
        return bool(set(requisito).intersection(set(ramos)))
    elif logico == 'y':
        print(bool(set(requisito).intersection(set(ramos))))
        return set(requisito).issubset(set(ramos))
    return requisito in ramos


def posicion_corte(requisito):
    requisito = requisito[1:] if requisito[0] == '(' else requisito
    while True:
        pos = requisito.find(')')
        if '(' not in requisito[:pos]:
            break
        requisito = requisito.replace(')', '|', 1).replace('(', '|', 1)
    return pos + 1


def cumple(ramos, requisito):
    requisito = requisito.replace(' ', '').replace('(c)', '[c]')
    if '(' not in requisito:
        if 'o' in requisito:
            req = requisito.split('o')
            return final(ramos, 'o', req)
        elif 'y' in requisito:
            req = requisito.split('y')
            return final(ramos, 'y', req)
        else:
            return final(ramos, '-', requisito)
    if '(' in requisito and ')' in requisito:
        pos = posicion_corte(requisito)
        derecha = requisito[pos + 1:]
        izquierda = requisito[1:pos]
        print('\n1', izquierda, '---', derecha, 'req:', requisito)
        if len(derecha) > 0:
            logico = derecha[0]
            derecha = derecha[1:]
            if logico == 'y':
                print('\n2', izquierda, '-y-', derecha)
                return cumple(ramos, izquierda) and cumple(ramos, derecha)
            elif logico == 'o':
                print('\n3', izquierda, '-o-', derecha)
                return cumple(ramos, izquierda) or cumple(ramos, derecha)
        return cumple(ramos, requisito[1:-1])

    return False

# print(cumple(ramos_alumno, req2))

# print('yuhu')

print(cumple(ram, req3))
