# -*- coding: utf-8 -*-
from collections import defaultdict
from babel.dates import format_date, format_datetime, format_time
import hashlib
import string
import datetime
import random
import csv
import os
import paramiko

# for ide
if False:
    import subprocess
    from gluon import TABLE, TR, TD, MARKMIN, A, URL, DIV, XML
    from gluon import session
    from db import configuration
    from log import log

# directorios
files_dir = 'applications/' + str(configuration.get('app.name')) + '/files/'

# websocket
# from gluon.contrib.websocket_messaging import websocket_send

valid_chars1 = (string.ascii_uppercase + string.digits +
                string.ascii_lowercase)


def tree():
    return defaultdict(tree)

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def md5sum(filepath):
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)


def idtemp_generator(size=50, chars=valid_chars1):
    """genero id random con marca de tiempo"""
    dia = (str(datetime.datetime.now().year) + '-' +
           str(datetime.datetime.now().month) + '-' +
           str(datetime.datetime.now().day) + '_')
    return dia + ''.join(random.choice(chars) for _ in range(size))


def hoy_string():
    dia = (str(datetime.datetime.now().year) + '-' +
           str(datetime.datetime.now().month) + '-' +
           str(datetime.datetime.now().day))
    return dia


def str_to_date(date_string):
    return(datetime.datetime.strptime(date_string, '%Y-%m-%d').date())


def dict_to_table(diccionario, orden=[], id=id):
    '''recibe un diccionario y devuelve una tabla html 2xn'''
    if type(diccionario) == dict:
        claves = diccionario.keys()
        aux_filas = []
        for i in reversed(orden):
            try:
                claves.insert(0, claves.pop(claves.index(i)))
            except Exception:
                pass
        for i in claves:
            aux_filas.append(TR(TD(i), TD(diccionario[i])))
        return TABLE(aux_filas, _id=str(id))
    elif type(diccionario) == str:
        return diccionario
    else:
        # aux_filas=['error',str(diccionario)]
        aux_filas = [TR(TD('bug!'), TD(str(diccionario)))]
        return TABLE(aux_filas, _id=str(id))


def list_of_dict_to_csv(nombre, lista, **kwargs):
    """recibe nombre y una lista de dicts y lo graba en disco,
    devuelve string nombre+hash"""
    if 'dir' in kwargs:
        directorio = str(kwargs['dir'])
    else:
        directorio = ('applications/' + str(configuration.get('app.name')) +
                      '/files/csv/')
    if 'norandom' in kwargs:
        nombre_archivo = str(nombre) + '.csv'
    else:
        nombre_archivo = str(nombre) + '_' + str(idtemp_generator(10)) + '.csv'
    subprocess.run(["mkdir", "-p", directorio])
    filepath = directorio + nombre_archivo
    try:
        keys = lista[0].keys()
        with open(filepath, 'w',
                  encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(lista)
            log(f'generado {filepath}')
            return ['ok', filepath]
    except Exception as e:
        log(e.args)
        return ['error', e.args]


def test_list_of_dict_to_csv():
    lista = [{'cantidad': 3,
              'cliente': 'PANIFICADORA ÑESTADIO S.A.',
              'fa_n': '0010000400000000000000003892',
              'fecha': datetime.date(2019, 2, 1),
              'lote': ['32'],
              'producto': 'TPC300x16'},
             {'cantidad': 20,
              'cliente': 'VASCO RAMON FERNANDO',
              'fa_n': '0010000400000000000000003893',
              'fecha': datetime.date(2019, 2, 2),
              'lote': ['33'],
              'producto': 'TDC123x18'}]
    return list_of_dict_to_csv('test', lista)


def list_dict_to_table_sortable(lista, nombre_archivo, **kwargs):
    '''recibe una lista de diccionarios(clave-valor iguales)
    y devuelve una tabla html'''
    if type(lista) == list:
        if type(lista[0]) == dict:
            claves = lista[0].keys()
            if 'orden' in kwargs:
                orden = kwargs['orden']
            else:
                # valores por defecto
                orden = ['dni', 'usuario', 'apellido y nombre', 'apellido',
                         'nombre', 'nombre map', 'baja map', 'reparticion',
                         'Unif', 'Unif_creado', 'Unif_modificado']
            for i in reversed(orden):
                try:
                    claves.insert(0, claves.pop(claves.index(i)))
                except Exception:
                    pass
                    # log(e)
            # cabecera tabla
            tabla = '<table data-toggle="table"> <thead> <tr>'
            for i in claves:
                fila = """<th data-field="%s" data-sortable="true">
                       %s</th>""" % (i, i)
                tabla = tabla + fila
            tabla = tabla + '</tr> </thead> <tbody>'
            # contenido tabla
            for i in lista:
                tabla = tabla + '<tr>'
                for j in claves:
                    tabla = tabla + '<td>%s</td>' % (i[j])
                tabla = tabla + '</tr>'
            tabla = tabla + '</tbody> </table>'
            cantidad = len(lista)
            leyenda_cantidad = (MARKMIN("Cantidad de dias registrados: " +
                                str(cantidad)))
            session.nombre_archivo = list_of_dict_to_csv(
                nombre_archivo, lista)[1]
            # open_archivo = open(dir_files + session.nombre_archivo, "r")
            boton_csv = A('Descarga tabla como CSV...',
                          _href=URL('descarga_csv'),
                          _class='btn btn-default')
            # return CENTER(TABLE(boton_csv,XML(tabla)))
            return DIV(boton_csv, leyenda_cantidad, XML(tabla))


def test_list_dict_to_table_sortable1():
    lista = [{'cantidad': 3,
              'cliente': 'PANIFICADORA ÑESTADIO S.A.',
              'fa_n': '0010000400000000000000003892',
              'fecha': datetime.date(2019, 2, 1),
              'lote': ['32'],
              'producto': 'TPC300x16'},
             {'cantidad': 20,
              'cliente': 'VASCO RAMON FERNANDO',
              'fa_n': '0010000400000000000000003893',
              'fecha': datetime.date(2019, 2, 2),
              'lote': ['33'],
              'producto': 'TDC123x18'}]
    claves = lista[0].keys()
    return list_dict_to_table_sortable(lista, 'test', claves)


def todos_los_archivos(directorio):
    archivos = []
    for path, subdirs, files in os.walk(directorio):
        for name in files:
            archivos.append(os.path.join(path, name))
    return archivos


def csv_to_list_of_dict(pathfile):
    """Lee archivo csv y devuelve lista ordenada"""
    lista = []
    try:
        with open(pathfile, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for dct in map(dict, reader):
                lista.append(dct)
            return ['ok', lista]
    except Exception as e:
        return ['error', str(e)]


def test_csv_to_list_of_dict():
    csvfile = 'applications/tapa14/files/csv-base/db_tipos_cuenta.csv'
    return csv_to_list_of_dict(csvfile)


def fecha_sp(datetime):
    fecha = datetime.date()
    return format_date(fecha, locale='es')


def datetime_sp(datetime):
    return format_datetime(datetime, locale='es')


def time_sp(datetime):
    time = datetime.time()
    return format_time(time, locale='es')


def s_horario(horario):
    return f'{time_sp(horario[0])} a {time_sp(horario[1])}'


def cred(server):
    if server == 'pegasus':
        return {
            'host': configuration.get('datos.ssh_host'),
            'user': configuration.get('datos.ssh_user'),
            'pass': configuration.get('datos.ssh_pass'),
            'port': configuration.get('datos.ssh_port')
        }


def ssh_command(server, command):
    "ejecuta command en server y devuelve {'stdout':stdout, 'stderr':stderr}"
    hostname = cred(server)['host']
    username = cred(server)['user']
    password = cred(server)['pass']
    port = cred(server)['port']
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(hostname, port=port,
                       username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        salida = {'stdout': stdout.read(), 'stderr': stderr.read()}
        client.close()
        return salida
    finally:
        client.close()
