## Requerimientos

Instalacion docker
* https://docs.docker.com/engine/install/debian/
* https://docs.docker.com/engine/install/ubuntu/

Instalacion docker compose v2 (cli-command)
* https://docs.docker.com/compose/cli-command/#install-on-linux

## Instalacion

### Copiar y configurar .env
```
cp conf/env.ejemplo .env
```
### Crear certificados locales
```
make genero-certs 
```
### Creo/instalo imagenes
```
make install
```


## Import de datos
clonar repo de datos

```
git clone git@github.com:redondomarco/tapa14-files.git data/files
```

copiar ultimos csv a

### Generar venv configurado en .vscode/settings.json
Entramos en bash del contenedor
```
make consola
```
Dentro, creamos virtualenv,lo activamos e instalamos dependencias para la ruta
./data/home/tapa14env/lib/python3.9site-packages/

```
virtualenv -p=/usr/bin/python3.9 /home/web2py/tapa14env
source /home/web2py/tapa14env/bin/activate
pip3 install -r /web2py/requirements.txt
exit
```
Salimos del virtualenv y dentro de la carpeta ./data/home/
clonamos el framework web2py para la ruta
```
cd data/home
git clone --recursive https://github.com/web2py/web2py.git
```

## Actualizacion web2py/gluon/yatl

### Revisar versiones
* https://github.com/web2py/web2py/tags
* https://github.com/web2py/pydal
* https://github.com/web2py/yatl
Cambiar la version en .env

hacer pull en ./data/home/ para venv
