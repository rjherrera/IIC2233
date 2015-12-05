Tarea 7
=======

## Interfaz

La interfaz es bastante sencilla, cuenta en primer lugar con una sección para ingresar, en la que se pide el código de autorización al usuario, de modo que se despliega la página de Dropbox correspondiente para darle permiso a la aplicación.

La segunda parte de la interfaz corresponde a una vez ingresado, donde se muestran los archivos y directorios, el nombre usuario en cuestión, una barra de progreso en caso de que se esté realizando alguna tarea, un botón para desloguearse y ciertos mensajes que indiquen información relevante.

En ciertos casos se abrirán ventanas emergentes cuando sea necesario pedir información adicional al usuario o darle cierta información.

## Visualización

Se muestran los archivos y carpetas en forma de árbol, y en ese arbol se maneja toda la aplicación. Al hacer click derecho en un archivo o carpeta, se muestran las posibles opciones a realizar con dicho elemento. El funcionamiento es el clásico desplegar/contraer.

## Login

Se implementa el sistema de autorización de Dropbox (oauth2) de modo que se muestra la página web para autorizar y una vez que el usuario obtiene el código, lo debe ingresar en el input correspondiente y aceptar. Una vez que se ha realizado el proceso, la autorización se guarda en el equipo del usuario de modo que no tenga que realizar cada vez el proceso.

## Funciones

Las funciones particulares para cada archivo se realizan al hacer click derecho en cada uno de ellos. Todas las funciones que lo requieran, son realizadas en Threads separados para así permitir que se pueda utilizar la aplicación mientras se realice alguna actividad pesada. Por ejemplo descargar una carpeta pesada y luego subir un archivo se puede realizar paralelamente.

### Descarga

Se pueden descargar tanto archivos como carpetas. El usuario debe elegir un destino y el archivo se descargará. En caso de ser carpeta, debe elegir una carpeta dentro de la cual se descargará (creará) la carpeta que está descargando.

### Subida

Se pueden subir archivos a las diferentes carpetas, el usuario debe seleccionar una carpeta y luego escoja un archivo local que se subirá dentro de la carpeta de destino antes elegida. Se usó este método en vez de que se cree en el mismo directorio de la carpeta elegida (se crea dentro) ya que de crearse "paralelamente" y no dentro, las carpetas nuevas no se podrían llenar de archivos inmediatamente y sería tedioso. Es por esto que la opción del menú solo aparece al seleccionar carpetas y dice "Upload file to folder", especificando que es A esa carpeta.

### Eliminar

Se agregó la funcionalidad extra de eliminar, que es bastante intuitiva, se debe seleccionar lo que se desee y esto lo eliminará. En caso de ser una carpeta se advierte de que la eliminación es recursiva, es decir elimina todo en su interior.

### Renombrar

Para renombrar, al usuario se le pide en una ventana emergente el nuevo nombre, se pueden renombrar tanto carpetas como archivos.

### Crear carpetas

Para crear carpetas, el usuario puede seleccionar una carpeta o archivo, de modo que la nueva carpeta quedará ubicada en el mismo directorio del elemento seleccionado. Se le pide un nombre para la nueva carpeta en una ventana emergente.

### Mover

Para mover archivos o carpetas se le pregunta al usuario la ruta de destino, seleccionándola en una ventana emergente, en la cual se cargan solamente los directorios.

### Historial

Al ver el historial de un archivo se muestra la última edición en el servidor y en algún cliente. Además se incluye el dato del tamaño del archivo. En el caso de las carpetas, se muestra la edición más reciente de cualquier archivo adentro de la carpeta, junto con especificar cual es ese archivo causante de la última modificación, también se muestra el tamaño de la carpeta. Se decidió hacerlo de esta manera para mantener la cohesión entre historial de archivo y carpeta, de modo que se muestre más o menos la misma información en cada caso.

## Código

Se entrega la interfaz general en un archivo [main.py](main.py). En otro archivo [widgets.py](widgets.py), que está explicado en ciertas zonas con comentarios y strings explicativos, se incluyen los widgets principales, el de login y el de archivos/funcionalidades en sí. De todos modos es un archivo bastante largo ya que la interfaz en sí contiene muchas funciones propias de ella y no supe como separarlo sin que perdiera sentido.

Se entrega un módulo [utils.py](utils.py) que contiene un par de funciones o clases extras, útiles para no sobrecargar más aún el archivo principal.

Se entregan también archivos [login_widget.ui](login_widget.ui) y [options_widget.ui](options_widget.ui) que contienen las interfaces creadas con QtDesigner, y que son cargados para generar los widgets.

### Explicación métodos

En general los métodos de mover archivos, descargar, etc. siguen esta lógica: un método que obtiene las cosas necesarias del usuario o del programa, y que ejecuta un Thread que llama al método helper, el que se encarga de hacer el request y de dar por finalizada la acción, con los cambios que eso implique.

##### Ejemplo:

###### Método:
```python
create_folder(self, item)
```
Se encarga de pedir el nombre de la carpeta al usuario
###### Método helper:
```python
create_folder_helper(self, new_path, new_name, item)
```
Se encarga de llamar a la API y crear la carpeta, y finalmente poner en el árbol de directorios el nuevo item, aparte de mover la barra de progreso. Se realiza en una sentencia try-except, al menos la parte referida a el request, se hace un except genérico porque los Exceptions que levanta Dropbox eran demasiados y no era la idea llenar de importaciones de Exceptions el programa.