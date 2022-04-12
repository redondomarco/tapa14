## Requerimientos

Instalacion docker
https://docs.docker.com/engine/install/debian/
https://docs.docker.com/engine/install/ubuntu/

Instalacion docker compose v2 (cli-command)
https://docs.docker.com/compose/cli-command/#install-on-linux

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
