### Distribución de puntajes

Requerimientos (**R**):

* **(1.00 pts)** R1: Correcta modelación de clases y relaciones
* **(0.75 pts)** R2: Correcto funcionamiento del ID
* **(1.50 pts)** R3: Lectura del archivo hasta línea correcta (con impresión del número de líneas leídas).
* **(0.75 pts)** R4: Es posible iterar correctamente sobre los pacientes de un Reporte
* **(1.00 pts)** R5: Retorar lista de color determinado correctamente
* **(1.00 pts)** R6: Impresión correcta de un paciente

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | Descuento |
|:--------|:--------|:--------|:--------|:--------|:--------|:--------|
| 1.0 | 0.6 | 1.0 | 0.75 | 1.0 | 1.0 | 0 |

| Nota |
|:-----|
| **6.35** |

### Comentarios
Sobre el id hiciste un método que funciona pero no es del todo correcto ya que la idea es que la misma clase lleve un conteo de sus instancias, mira este ejemplo:

class Paciente:
    identificador = id_paciente()

    def id_paciente():
        identificador = 0

        while True:
            yield identificador
            identificador += 1

y en el __init__ llamarlo así
    self.id = next(Paciente.identificador)

Sobre la lectura del archivo, bastante bien pero hay 2 problemillas. El primero es que estas creando las instancias de Paciente incluso cuando no las vas a utilizar, eso no es ni elegante ni eficiente y el segundo es que no estás llevando la cuenta de cuantas lineas se leyeron en total, información que puede ser muy relevante (además que lo pedían en el enunciado)

El resto está muy bien! muy buena actividad felicitaciones


