# -*- coding: utf8 -*-
from zlib import compress, decompress, crc32


class InstaPUC:

    @staticmethod
    def getData(filename):
        signature = None
        ihdr = {}
        idat = bytearray()
        iend = None
        with open(filename, 'rb') as file:
            signature = file.read(8)
            i = 1
            while True:
                largo = int.from_bytes(file.read(4), byteorder='big')
                tipo = file.read(4).decode('utf-8')
                print(tipo)
                if tipo == 'IHDR':
                    ancho = int.from_bytes(file.read(4), byteorder='big')
                    alto = int.from_bytes(file.read(4), byteorder='big')
                    prof = int.from_bytes(file.read(1), byteorder='big')
                    colores = int.from_bytes(file.read(1), byteorder='big')
                    compresion = int.from_bytes(file.read(1), byteorder='big')
                    filtro = int.from_bytes(file.read(1), byteorder='big')
                    entrelazado = int.from_bytes(file.read(1), byteorder='big')
                    ihdr = {'ancho': ancho, 'alto': alto,
                            'profundidad': prof, 'colores': colores,
                            'compresion': compresion, 'filtro': filtro,
                            'entrelazado': entrelazado}
                    i += 1
                elif tipo == 'IDAT':
                    idat = bytearray(file.read(largo))
                elif tipo == 'IEND':
                    # iend = file.read(0)
                    break
                else:
                    file.read(largo)
                crc = file.read(4)
        return signature, ihdr, decompress(idat), iend

    @staticmethod
    def bytes2matrix(ihdr, idat):
        matriz = []
        ancho = ihdr['ancho']
        for i in range(ihdr['alto']):
            fila = []
            for j in range(ancho):
                # x = idat[1+i:1 + 3*j + i]
                x = idat[1 + i * ancho:1 + i * ancho + 1]
                y = idat[1 + i * ancho + 1:1 + i * ancho + 2]
                z = idat[1 + i * ancho + 2:1 + i * ancho + 3]
                x = int.from_bytes(x, byteorder='big')
                y = int.from_bytes(y, byteorder='big')
                z = int.from_bytes(z, byteorder='big')
                # matriz[i][j - 1] = (x, y, z)
                fila.append((x, y, z))
            matriz.append(fila)
        ########################################
        #                                      #
        # Completar método.                    #
        # Transformar arreglo de bytes a una   #
        # matriz de pixeles.                   #
        #                                      #
        ########################################
        return matriz

    @staticmethod
    def matrix2string(matriz):
        # Este método transforma la matriz en un string de bytes.
        out = b''
        for i in range(len(matriz)):
            out += (0).to_bytes(1, byteorder='big')
            for j in range(1, len(matriz[i])):
                for k in matriz[i][j]:
                    out += k.to_bytes(1, byteorder='big')
        return out

    @staticmethod
    def rotate(ihdr, matriz):
        salida = []
        for i in range(len(matriz[0])):
            fila = []
            for j in matriz:
                fila.insert(0, j[i])
            salida.append(fila)
        return ihdr, salida

    @staticmethod
    def grey(ihdr, matriz):
        salida = [[i for i in range(len(matriz[0]))] for j in range(len(matriz))]
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                pr = (matriz[i][j][0] + matriz[i][j][1] + matriz[i][j][2]) // 3
                salida[i][j] = (pr, pr, pr)
        ihdr['colores'] = 0
        return ihdr, salida

    @staticmethod
    def writeImage(outFile, signature, ihdr, idat, iend):
        idat = compress(idat, 9)
        with open(outFile, 'wb') as file:
            file.write(signature)
            file.write(ihdr)
            file.idat(idat)
            file.write(iend)
        ########################################
        #                                      #
        # Completar método.                    #
        # Escribe un nuevo archivo PNG con la  #
        # información entregada.               #
        # TIP: No es necesario hacer varios    #
        # chunks de IDAT.                      #
        #                                      #
        ########################################
        print("Tu imagen ha sido transformada exitosamente!")


if __name__ == '__main__':

    imagefile = 'Mushroom.png'  # Mushroom.png o MickeyMouse.png

    firma, ihdr, data, end = InstaPUC.getData(imagefile)

    matriz = InstaPUC.bytes2matrix(ihdr, data)

    ihdr_gris, matriz_gris = InstaPUC.grey(ihdr, matriz)

    idat_gris = InstaPUC.matrix2string(matriz_gris)

    InstaPUC.writeImage(
        'image.png',
        firma,
        ihdr_gris,
        idat_gris,
        end)

"""
    # Descomentar si se realiza el bonus

    ihdr_gris_rotado, matriz_gris_rotada = InstaPUC.rotate(
        ihdr_gris, matriz_gris)

    idat_gris_rotado = InstaPUC.matrix2string(matriz_gris_rotada)

    InstaPUC.writeImage(
        'image.png',
        firma,
        ihdr_gris_rotado,
        idat_gris_rotado,
        end)
"""
