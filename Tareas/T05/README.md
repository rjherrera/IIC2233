Tarea 5
============

## Detalles interfaz

Se tiene una pantalla de inicio donde se explica la dinámica (se hizo el juego en ingles en general) y se muestra un boton para jugar, junto con el máximo puntaje alcanzado hasta la fecha.


## PYTQ4 y Compatibilidad

Se realizó todo con PYQT4 junto con QTDesigner y fue probado en Ubuntu, por lo que quizás en Windows u OSX, las labels, progressbars, etc. se vean descuadradas.

## Consideraciones

El juego considera un personaje principal (un Skeleton Mage) animado, que dispara balase desde su varita mágica y que tiene un máximo de 30 balas, junto con un máximo de 100 de vida. Cada ataque de zombie implica 30 de disminución para que tema por su vida y cada bala, claramente implica 1 de disminución en la barra.

## Movimiento

El personaje principal sigue al mouse y las teclas cambian su comportamiento dependiendo de la orientación del jugador. Se implementó un sistema de sprites que considera los pasos del usuario junto con animaciones tales como atacar (al disparar) y morir.

## Zombies

Los zombies aparecen según una función que depende del tiempo de juego en una zona de los bordes aleatoriamente definida y están animados de forma que se mueven, atacan y mueren.

## Balas

Las balas como se dijo en el enunciado llegan no hasta el infinito pero como el terreno de juego era chico se consideró que alcanzan a salir de la pantalla. Por lo que se eliminan las balas posteriormente

Las balas matan de un tiro a los zombies si le achuntan, y siguen una trayectoria rectilínea desde el usuario hacia el zombie

## Care Packages

El helicoptero tira care packages aleatorios entre comida y balas cada uno con su imagen distinta, los valores son aleatorios (randint) entre 10 y 20 si son puntos de salud, y entre 5 y 10 si es munición. Si se llega a el se gana lo que otorga el paquete, sino se queda hasta que aparezca otro (es como si se desvaneciera justo antes de que aparezca el otro para que el usuario no pueda acumular y guardar para cuando necesite, y así se haga mas difícil). El tiempo entre ellos también es aleatorio y se define cada vez que un package es tirado, sin embargo el primero es fijo a los 30 segundos.

## Puntaje

El puntaje se actualiza de modo que está en función del tiempo y los zombies asesinados, pero se muestra entero ya que cada segundo se agregan 0.25 puntos al puntaje, pero solo se muestra cuando se hayan juntado 4, para no tener decimales.

## Guardado de scores

Se guarda el mejor puntaje con pickle, y se carga cada vez que se juega.

## Colisiones

Se implementa un sistema en el que para dar harta libertad de escape al usuario, solo si se está topando de frente con un zombie no se puede continuar moviendo. En cambio para los zombies es diferente, si estan cerca del usaurio lo atacan, pero si topan con otro zombie no buscan otro camino sino que se quedan en cola esperando. La idea era dar libertad al usuario por sobre el zombie.


## Orden del código

Si bien el main es bastante extenso es porque la mayoría de las cosas las iba haciendo en la ventana misma, osea en la aplicación. Quizás se pudo haber modularizado más pero no se me ocurrió como realizar las tareas de pyqt en otro archivo y unirlo finalmente. De todos modos tiene hartos comentarios para que no sea tan ardua la corrección, lo siento si es muy largo el código, no fue mi intención, siempre intento ser ordenado. Las cosas que si se pudieron hacer afuera, como clases y funciones auxiliares, están presentes tanto en el archivo [utils.py](utils.py) como en [sprites.py](sprites.py), y las imagenes junto con los scores guardados en la carpeta sources [sources](sources)
