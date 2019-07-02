# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
import hashlib
import string
import datetime
import random
import csv
import os

# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

# directorios
files_dir = 'applications/' + str(configuration.get('app.name')) + '/files/'

# logs
logger = logging.getLogger("web2py")
logger.setLevel(logging.DEBUG)
log_remove = [
    'Set-Cookie: ',
    'session_id_tapa14=']


def log(palabra):
    """funcion auditoria que incorpora el usuario si es que existe"""
    if hasattr(auth.user, 'email'):
        mensaje = (str(auth.user.email) + ' '
        + str(request.function) + ' ' + str(palabra))
        for i in log_remove:
            mensaje = mensaje.replace(str(i), '')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin ' + str(palabra))


def debug(palabra):
    if hasattr(auth.user, 'email'):
        mensaje = 'DEBUG-' + str(palabra) + '-FIN'
        for i in log_remove:
            mensaje = mensaje.replace(str(i), '')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin ' + str(palabra))

# websocket
# from gluon.contrib.websocket_messaging import websocket_send


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


def idtemp_generator(
    size=50,
    chars=(string.ascii_uppercase + string.digits +
           string.ascii_lowercase)):
    dia = (str(datetime.datetime.now().year) + '-' +
           str(datetime.datetime.now().month) + '-' +
           str(datetime.datetime.now().day) + '_')
    return dia + ''.join(random.choice(chars) for _ in range(size))


def hoy_string():
    dia = (str(datetime.datetime.now().year) + '-' +
           str(datetime.datetime.now().month) + '-' +
           str(datetime.datetime.now().day))
    return dia


def dict_to_table(diccionario, orden=[]):
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
        return TABLE(aux_filas, _id="tabla_informe")
    elif type(diccionario) == str:
        return diccionario
    else:
        # aux_filas=['error',str(diccionario)]
        aux_filas = [TR(TD('bug!'), TD(str(diccionario)))]
        return TABLE(aux_filas, _id="tabla_informe")


def list_of_dict_to_csv(nombre, lista, **kwargs):
    """recibe nombre y una lista de dicts y lo graba en disco,
    devuelve string nombre+hash"""
    if 'dir' in kwargs:
        directorio = str(kwargs['dir'])
    else:
        directorio = 'applications/' + str(configuration.get('app.name')) + '/files/csv/'
    if 'norandom' in kwargs:
        nombre_archivo = str(nombre) + '.csv'
    else:
        nombre_archivo = str(nombre) + '_' + str(idtemp_generator(10)) + '.csv'
    log(directorio + nombre_archivo)
    try:
        keys = lista[0].keys()
        with open(directorio + nombre_archivo, 'w',
                  encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(lista)
            return ['ok', nombre_archivo]
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



def list_dict_to_table_sortable(lista):
    '''recibe una lista de diccionarios(clave-valor iguales) y
     devuelve una tabla html'''
    if type(lista) == list:
        if type(lista[0]) == dict:
            claves = lista[0].keys()
            orden = ['fecha', 'dni', 'usuario', 'apellido y nombre',
                     'apellido', 'nombre']
            for i in reversed(orden):
                try:
                    claves.insert(0, claves.pop(claves.index(i)))
                except Exception:
                    pass
                    # log(e)
            # cabecera tabla
            tabla = '<table data-toggle="table"> <thead> <tr>'
            for i in claves:
                tabla = tabla + '<th data-field="%s" data-sortable="true">%s</th>'%(i,i)
            tabla = tabla + '</tr> </thead> <tbody>'
            # contenido tabla
            for i in lista:
                tabla = tabla + '<tr>'
                for j in claves:
                    tabla = tabla + '<td>%s</td>' % (i[j])
                tabla = tabla + '</tr>'
            tabla = tabla + '</tbody> </table>'
            cantidad = len(lista)
            leyenda_cantidad = MARKMIN("Cantidad de registros analizados: " + str(cantidad))
            session.nombre_archivo = list_of_dict_to_csv('informe_documentos',lista)[1]
            # open_archivo = open('applications/' + str(configuration.get('app.name')) + '/files/csv/'+session.nombre_archivo, "r")
            boton_csv = A('Descarga tabla como CSV...',
                          _href=URL('descarga_csv'),
                          _class='btn btn-default')
            # return CENTER(TABLE(boton_csv,XML(tabla)))
            return DIV(boton_csv, leyenda_cantidad, XML(tabla))


def todos_los_archivos(directorio):
    archivos = []
    for path, subdirs, files in os.walk(directorio):
        for name in files:
            archivos.append(os.path.join(path, name))
    return archivos
