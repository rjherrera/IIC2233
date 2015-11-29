# Tarea 6

## Chat

Para ahorrarte el trabajo, estimado ayudante corrector jajaj, decirte que empecé el mismo día así que mucho no hice, por no decir nada, no pude empezar antes por diversos problemas y no pretendo piedad ni nada, solo aviso para ahorrarte tiempo. Empecé a hacer un chat con su respectiva interfaz y que se pudiera comunicar con los otros usuarios, sin embargo no alcancé a terminarlo, lo que si funciona es el sistema de usuarios.

En general el sistema se basa en mandar instrucciones seguidas de contenido, por ejemplo: 'LOGIN|USERNAME|PASSWORD' para hacer un split después, etc.

Se guardan los usuarios pickleados y se cargan igualmente.

Para el cliente se necesita el archivo .ui, el cliente.py y el utils.py, para el servidor el servidor.py y el utils.py

Modificar el utils.py para el tema del port y host

### Login

Se verifica que exista el usuario y de existir verifica la password, todo utilizando un sistema de hasheo con salt en el cual se itera muchas veces para hacerlo más seguro (según leí en internet)

### Signup

Se crea el usuario verificando los requisitos para pass y username y se loguea automaticamente, tambien la clave no se guarda, sino que un hash de ella. El sistema guarda en los usuarios un artibuto salt, para que sea un poco menos vulnerable que usar un salt generico, se usa el sistema per_user_salt, cosa que si bien el programa puede ser vulnerable a ataques de fuerza bruta, no pueden ser simultaneos con el mismo salt los ataques y además como se itera para crear el hash, es más lento que un hasheo normal por lo que es menos vulnerable.

### Funcionamiento chat

La idea era que en ese combobox salieran los usuarios y al apretar uno se actualiza el text browser con el texto del historial y empieza el flujo de msjes

### Emojis

Se empezó a hacer lo de los emojis, la idea es en un dicc poner el unicode de los emojis, para dps reemplazarlo en el html del visor del chat