Tarea 1
============

## Detalles interfaz

Los sistemas de toma de ramos en esta tarea se ejecutan desde [main.py](main.py) de modo que en un principio se cargan los datos y luego permite el acceso a ellos. Se ingresa con una contraseña que debido a limitaciones de librerías externas se mantiene visible.

Cuando uno ingresa al sistema, éste identifica si se trata de un profesor o un alumno, en caso de ser profesor, como únicas opciones permite dar y quitar permisos. En cambio, si se ingresa como alumno, nos pregunta sobre el el tiempo del día (al ejecutar el programa se entiende mejor), para decidir si ir a Pacmático o Bummer.

### Bummer

Dentro de Bummer, se permite tomar ramos, botarlos y generar horarios o calendarios. Cuando se decide ingresar o a tomar o a botar ramos, el sistema pregunta por una hora, la cual, de ser correspondiente al horario de inscripcion del alumno se guarda temporalmente por 3 minutos, para salir y entrar sin problemas durante ese lapso, hasta que vuelve a pedirla en caso de querer volver a entrar a la toma de ramos.

Los ramos se toman ingresando la sigla y la sección con guión opcional (IIC2233-2 es válido, tanto como fis15134). El horario se genera en consola, pero de querer exportarlo se guarda en la ruta "files/horario_timestamp.txt" para evitar problemas de sobreescritura.

Los requisitos de un ramo se revisan recursivamente, y para facilitar las situaciones relacionadas con requisitos se optó por agregar a la lista de cursos_aprobados perteneciente a la clase Alumno, los cursos con la marca '[c]' al final, para que al comprobar si cumple el requisito, aparezca verdadero, de haber tomado el ramo el presente semestre.

Al salir del sistema se alerta al usuario en caso de no contar con 30 créditos tomados.

### Pacmático

Dentro de Pacmático se permite agregar o sacar cursos a una distribución de cursos, y redistribuir los puntos que se le otorgan a cada ramo, también se da la opción de resetear la redistribución equitativamente.

Para el cálculo de los puntos del usuario en cuanto a la formula que involucra créditos y bacanosidad relativa, se optó por asumir que todos los cursos cuentan con 10 créditos ya que muchos de los cursos presentes en la lista de cursos aprobados de cada alumno, no están presentes en ninguna parte, como para saber los créditos que acumulan. Es por eso que se opta por esa simplificación, que por lo demás no parece ser muy lejana a la realidad.

Finalmente se permite obtener la distribución de ramos final, de modo que les hubiesen dado los cursos a los alumnos, pero para esto se requiere del uso prolongado del sistema (tomar ramos con múltiples usuarios).

#### Aclaraciones

Para la comprobación de requisitos en cuanto a equivalencias se simplificó ya que se pudo comprobar en el archivo de requisitos, que en todos los ramos que había equivalencias, estas equivalencias estaban marcadas dentro del requisito de la forma "Ramo o Ramo_Equivalente o Ramo_Antiguo" de modo que no es necesario realizar procesamiento adicional de ellas, ya que al procesarse como requisitos, de estar en la lista de cursos aprobados por el alumno, va a funcionar.

El calculo de bacanosidad transversal a ambos se realiza con matrices y sólo en el caso de no encontrar el archivo [bacanosidad.txt](files/bacanosidad.txt) presente en la carpeta files. Se hace una matriz de relaciones, de forma que existen 1's si se considera ídolo a un usuario y 0's de lo contrario, para luego normalizar por columna y efectuar cálculos de exponenciación de matrices usando numpy las suficientes veces como para tener valores adecuados (convergentes) de bacanosidad.