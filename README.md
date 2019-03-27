# tapa14
sistema integral stock para pyme: -en desarrollo-
- stock
- generacion de iva ventas a partir de archivos de RCEL

## Dependencias
### Sistema Operativo - debian stretch
```
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev python3-pip swig libssl-dev git unzip ipython3 python3-tk
```
### Parche M2Crypto ###
```
git clone https://github.com/mcepl/M2Crypto.git
cd M2Crypto
sudo python3 setup.py install
```
### requerimientos python3
```
pip3 install -r requirements.txt
```
### instalacion web2py
```
wget https://mdipierro.pythonanywhere.com/examples/static/web2py_src.zip
unzip web2py_src.zip
```
### descarga de app
```
cd web2py/applications
git clone https://github.com/redondomarco/tapa14.git
cd web2py/applications/tapa14/modules
git clone https://github.com/redondomarco/pyafipws.git
cd web2py/applications/tapa14/views
git clone https://github.com/redondomarco/plugin_adminlte
```
#### actualizacion de app
```
cd web2py/applications/tapa14
git pull
```

####configuracion de la app
Copiamos y editamos el archivo private/appconfig.ini
```
cp web2py/applications/tapa14/examples/appconfig.ini web2py/applications/tapa14/private/
```
#### ejecucion de la shell
web2py nos provee una shell -modelo incluido-
```
cd web2py
python3 web2py.py -S tapa14 -M
```
#### datos iniciales
Desde la shell importamos una base de datos inicial:
```
>>> db.import_from_csv_file(open('applications/tapa14/examples/tapa14_base.csv', 'rb'))
```
#### para exportar todas nuestras tablas
```
>>> db.export_to_csv_file(open('nuestras_tablas.csv', 'wb'))
```
