Tarea 3
============

## Detalles interfaz

El sistema se ejecuta desde [main.py](main.py) de modo que, en primer lugar, permite posicionar las naves de ambos jugadores y luego se procede a jugar por turnos. En un turno, o se ataca o se mueve una nave, siempre se puede ver el radar al principio, independiente de lo que se haga posteriormente.

Para hacerlo interesante se "borra" la pantalla 5 veces con la funcion de os para que así sea dificil ver la pantalla del rival (habría que retroceder[subir] 5 pantallas de la consola)

## Precisiones

Se hace que cada 4 turnos se borren los barcos muertos de forma que se pueda mover uno a donde hubo antes un barco, entonces duran ciertos turnos las "X" en los lugares donde hubo ataques.

Uno no sabe la resistencia de sus barcos para que así el juego tenga misterio y no dure tanto (no sabes cual te atacaron, tonces usar sanar del kit de ingenierios es dificil)

## Movimientos

No se terminó, casi funcional

## Ataques

Se creó una clase para cada ataque, se consideraron todas las precisiones, y el "ataque" de sanar.

## Radar

No se terminó, sin embargo se dejó avanzado con un diccionario que tiene todos los turnos.

## Estadísticas

No se terminó pero se tienen todos los datos en las distintas partes (especialmente en los ataques),
como para poder obtenerlos

## Testing

Muy poco testing, no se alcanzó a desarrollar más, sin embargo se tuvo el cuidado de tener las funciones sin inputs por el lado de los modulos tablero, vehiculos y ataques, de modo que los inputs solo estuvieran en main.py



# Por temas familiares/personales empecé la tarea el lunes 5, por eso la mediocridad. Lo siento :(