# Actividad 27

## Método de autenticación

Se elije el método de pasar los argumentos antes de inicializar el script, de modo que el usuario al ejecutar el script tenga que ingresar su clave y contraseña.

Debe ejecutar el script de esta manera:

## RESUMEN

```sh
python3 main.py obtener_votos -u <user> -p <password>
```


# EXPLICACION LARGA

## Usage:

See all available commands and options:
```
$ python3 main.py --help
```

Help menu:
```sh
usage: main.py [-h] -u USER -p PASSWORD [PASSWORD ...]

Votes system

positional arguments:
  obtener_votos         Obtener ganador de votos

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username for API
  -p PASSWORD , --password PASSWORD  Password for API

```

### Example:
#### Using full-name flags:
```sh
python main.py obtener_votos --user=User --password=password
```

#### Short version:
```sh
python main.py order -u User -p Password
```

Output:
```sh
Los votos totales son:
 Lista_n: votos
 ...
El que obtuvo el máximo fue: Lista con X votos.
```