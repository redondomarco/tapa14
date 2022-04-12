#!/bin/bash
echo instalo paquetes sistema operativo - base de datos incluida !
sudo apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3-dev python3-pip swig libssl-dev git unzip ipython3 python3-tk postgresql libpq-dev 2to3

echo instalo paquetes python
sudo pip3 install -r requirements.txt

echo
echo # configurar base de datos
echo sudo passwd postgres
echo su - postgres createuser -PE -s t14user
echo createdb -O t14user -E UTF8 tapa14v1
echo

cd ~/web2py/applications/tapa14
git clone https://github.com/redondomarco/tapa14-files.git files
echo
echo copiar logging.conf opcional - por defecto a file
echo para syslog copiar manualmente logging.conf-syslog apunta a local3
echo
cp ~/web2py/applications/tapa14/files/conf/logging/logging.conf-file ~/web2py/logging.conf
echo copio configuracion appconfig.ini inicial - configurar !!
mkdir -p ~/web2py/applications/tapa14/private
mkdir -p ~/web2py/applications/tapa14/databases
cp ~/web2py/applications/tapa14/files/conf/appconfig.ini ~/web2py/applications/tapa14/private/

echo Instalo frontail
echo comprobar ultimas versiones en https://github.com/mthenw/frontail/releases
cd ~
wget https://github.com/mthenw/frontail/releases/download/v4.9.0/frontail-linux
sudo chmod +x ~/frontail-linux
sudo mv ~/frontail-linux /usr/local/bin/frontail-linux

echo
echo Para usar frontail ejecutar: 
echo /usr/local/bin/frontail-linux -n 100 -l 3000 -d -t dark --ui-highlight ~/web2py/logs/web2py.log
echo

echo instalo conf ide wing
sudo ln -s ~/web2py/applications/tapa14/files/conf/wing/pylint-tapa14  /usr/local/bin/pylint-tapa14
sudo ln -s ~/web2py/applications/tapa14/files/conf/wing/pylint-personal /usr/local/bin/pylint-personal
