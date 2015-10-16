### Distribución de puntajes

Requerimientos (**R**):

* **(2.0 pts)** R1: Crear el método setUP y tearDown
* **(0.5 pts)** R2: Test de revisar_nombre 
* **(0.5 pts)** R3: Test de revisar_formato
* **(1.0 pts)** R4: Test de revisar_verificador
* **(1.0 pts)** R5: Test de revisar_orden
* **(1.0 pts)** R6: Test de descontar
* **(1.0 pts)** R7: Test de get_palabras y get_descuento (0.5 cada uno)
* **(1.0 pts)** BONUS: Crear nuevo programa corrector sin errores

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | R7 | BONUS | Descuento |
|:---|:---|:---|:---|:---|:---|:---|:------|:----------|
| 2.0 | 0.3 | 0.3 | 0.8 | 1.0 | 0 | 0.6 | 0 | 0 |

**Para un 7.0 se necesitan 7 puntos**

| Nota |
|:-----|
| 5.29 |

### Comentarios

Debiera detectar las funciones con error (FAILED (failures=4))
get_descuento, 
get_palabras, 
revisar_formato y 
revisar_nombre

        self.assertTrue(self.c1.revisar_nombre())
        self.assertTrue(self.c2.revisar_nombre())
        self.assertFalse(self.c3.revisar_nombre())
        self.assertTrue(self.c4.revisar_nombre()) 2 y 4 deben ser F

        self.assertTrue(self.c1.revisar_formato(self.c1.nombre.split('.')[-1]))
        self.assertTrue(self.c2.revisar_formato(self.c2.nombre.split('.')[-1]))
        self.assertTrue(self.c3.revisar_formato(self.c3.nombre.split('.')[-1]))
        self.assertFalse(self.c4.revisar_formato(self.c4.nombre.split('.')[-1])) 2 debe ser F, el resto T

        self.assertTrue(self.c1.revisar_verificador(self.c1.nombre.split('_')[0]))
        self.assertTrue(self.c2.revisar_verificador(self.c2.nombre.split('_')[0]))
        self.assertFalse(self.c3.revisar_verificador(self.c3.nombre.split('_')[0]))
        self.assertTrue(self.c4.revisar_verificador(self.c4.nombre.split('_')[0])) 4 debe ser F, el resto T
Hay error en los descuentos
En get_palabras debes comparar las palabras que realmente hay en el archivo. El método del main tiene error porque cuenta los espacios!


* Sin Comentarios
