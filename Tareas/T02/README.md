Tarea 2
============

## Detalles interfaz

El sistema se ejecuta desde [main.py](main.py) de modo que, en primer lugar, carga el sistema y realiza el mapeo de la red, para luego proceder a mostrar las distintas opciones de la tarea, como exportar los diferentes archivos.


## Estructuras de datos

En [lists.py](data_structures/lists.py) se encuentra la clase List que corresponde a mi propia versión de la lista ligada clásica, basado en el material de clases, implementa métodos como

```python
lista = List()
lista.append(5)
x = lista.popleft()
lista.append(10)
lista.remove(10)
len(lista)
lista.append(0)
lista[0]
```

Los cuales son bastante similares a los de list, pero remove por ejemplo retorna otra lista. Más detalles se desprenden de ejecutar el archivo [lists.py](data_structures/lists.py) desde ahí mismo.

En [trees.py](data_structures/trees.py) se encuentra la clase Arbol que corresponde también a una implementación basada en el material e implementa métodos tales como:

```python
arbol = Arbol()
arbol.add(5)
arbol.find(5)
5 in arbol
arbol[0]
len(arbol)
iter(arbol)
```

Para más info. también se puede ejecutar desde el mismo archivo [trees.py](data_structures/trees.py)

## Conexiones y Puertos

Se crearon las clases Conexion, Puerto, Ruta y Grafo en [grafo.py](grafo.py) con sus respectivos métodos para analizar y trabajar con la estructura de la red.

Para iterar y guardar datos de forma eficiente, se guardan dinámicamente los datos en los árboles binarios para revisar si existen y almacenar los datos lo más eficientemente posible.

### Puertos

El sistema en sí inspecciona toda la [red](sistema.pyc) en busca de puertos y conexiones, para obtener todos los puertos, se itera hasta obtener el último o puerto mayor, actualizando cada vez el valor de ese "máximo" actual. Se recorre aleatoriamente desde cada puerto, es decir se escoge dentro de las posibles conexiones de un puerto, una al azar para dirigirse.

### Conexiones

Para las conexiones se inspecciona de forma un poco distinta porque obtener el total de conexiones no es sencillo. Así para lograr esto, se recorre la red la cantidad de veces que sea necesario hasta obtener todos los puertos. La forma en que se consigue eso es iterando hasta que el número total de conexiones deje de cambiar (3 grupos seguidos de 200.000 iteraciones), es decir, en algún momento, si han pasado más de 600.000 iteraciones sin que cambie el número, se corta.

## Opciones Generales

Las siguientes opciones se encuentran implementadas como métodos de la clase Grafo

### Obtener la red

Para obtener la red primero se procede a obtener los puertos y las conexiones como se detalló anterior mente y luego, se decide cuales conexiones son alternantes, normales y random. Se hace por medio de un identificador propio en cada conexión que corresponde al numero que se obtiene al elegir una de las posibles conexiones del puerto de origen. Así, si dos o más conexiones tienen el mismo origen y el mismo identificador, corresponden a conexiones de tipo alternantes o aleatorias.

Para dirimir entre ambas, el criterio usado, debido a la imposibilidad de detectar el movimiento constante del robot, corresponde a que si una conexión cambia entre 2 puertos es alternante, y si cambia entre 3 o más es aleatoria, de no cambiar queda como normal

### Obtener la ruta mínima a Bummer

Para la ruta mínima se utiliza el algoritmo BFS de búsqueda por amplitud. A grandes rasgos en una especie de pila se introduce el primer puerto, y luego se agregan todos sus puertos aledaños. Después se saca el puerto y se introducen los puertos aledaños de cada uno de los siguientes puertos, comprobando en cada paso de no haber llegado al puerto final, el puerto de Bummer. A medida que se avanza siempre se va por niveles, de modo que nos aseguramos de estar siempre en la ruta más corta con la posibilidad de que existan otras rutas pero que estas sean mayores o iguales a la escogida. Implementación del algoritmo basada en respuesta de [stackoverflow](http://stackoverflow.com/a/8922151).

### Obtener rutas de doble sentido

Para esta sección se itera sobre todos los puertos, y a su vez sobre todos los puertos a los que ese puerto de origen llega, de modo de encontrar si en alguno de esos puertos existe como destino el puerto inicial. Se eliminan duplicados y se prefieren rutas mayores, eliminando rutas que sean subconjuntos de otras.

### Obtener ciclos triangulares y cuadrados

Aquí de forma similar se itera sobre los puertos para ver si cumplen la condicion de estar en conexiones cuadradas o triangulares. Se evitan duplicados por rotación para un triángulo ABC tales como BCA y CAB (CBA, BAC y ACB son triángulos distintos así que si pueden estar presentes). Análogamente para el cuadrado, solo rotaciones y no permutaciones se descartan. Para ambos casos, no se agregan conexiones en las que se de que puertos esten repetidos en el ciclo 1 o más veces.

### Obtener capacidad máxima

Para esta sección se procede a evaluar distintas rutas, obteniendolas extendiendo el BFS para que no se corte al encontrar el primer camino. Se obtienen varios caminos para luego comparar el flujo de cada uno de ellos y escoger el mayor. A modo de hacer más eficiente el algoritmo se dice que un camino tiene el flujo máximo inmediatamente si el flujo del camino es igual a uno de los dos extremos fijos, puerto inicial y puerto Bummer.

### Eliminar ciclos

Para eliminar los ciclos que hacen ineficiente a Bummer se opta por buscar los ciclos de profundidad menor que 100, es decir que se demoran hasta 100 conexiones en volver al puerto de origen. Luego se eliminan dichos puertos.

## Outputs

Los outputs de las distintas opciones se generan en los archivos especificados en el enunciado, al ejecutar la respectiva acción en el menu del programa.