#!/bin/bash
echo instalo paquetes sistema operativo - base de datos incluida !

apt-get update
apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3-dev python3-pip swig libssl-dev git unzip ipython3 postgresql libpq-dev 2to3 ssh zip unzip tar python3 ipython3 python3-dev apache2 wget curl bwm-ng vim git lnav dnsutils libapache2-mod-wsgi-py3 python3-psycopg2 postgresql-server-dev-all

echo instalo paquetes python
sudo pip3 install -r requirements.txt

echo
echo # configurar base de datos
echo sudo passwd postgres
echo su - postgres createuser -PE -s t14user
echo createdb -O t14user -E UTF8 tapa14v1
echo


echo descargo datos
echo
cd /home/www-data/web2py/applications/tapa14
git clone https://github.com/redondomarco/tapa14-files.git files
echo
echo copiar logging.conf opcional - por defecto a file
echo para syslog copiar manualmente logging.conf-syslog apunta a local3
echo
cp /home/www-data/web2py/applications/tapa14/files/conf/logging/logging.conf-file ~/web2py/logging.conf
echo copio configuracion appconfig.ini inicial - configurar !!
mkdir -p /home/www-data/web2py/applications/tapa14/private
mkdir -p /home/www-data/web2py/applications/tapa14/databases
cp /home/www-data/web2py/applications/tapa14/files/conf/appconfig.ini /home/www-data/web2py/applications/tapa14/private/

cp /home/www-data/web2py/applications/tapa14/files/conf/consola /usr/local/bin/consola
chmod +x /usr/local/bin/consola

chown -R www-data:www-data /home/www-data/web2py
