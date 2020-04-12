# -*- coding: utf-8 -*-
from collections import defaultdict
import hashlib
import string
import datetime
import random
import csv
import os

# for ide
if False:
    from gluon import TABLE, TR, TD, MARKMIN, A, URL, DIV, XML
    from gluon import session
    from db import configuration
    from log import log

# directorios
files_dir = 'applications/' + str(configuration.get('app.name')) + '/files/'

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
        directorio = 'applications/' + str(configuration.get('app.name')) + '/files/csv/'
    if 'norandom' in kwargs:
        nombre_archivo = str(nombre) + '.csv'
    else:
        nombre_archivo = str(nombre) + '_' + str(idtemp_generator(10)) + '.csv'
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


def list_dict_to_table_sortable(lista, nombre_archivo, claves):
    '''recibe una lista de diccionarios(clave-valor iguales) y
     devuelve una tabla html'''
    if type(lista) == list:
        if type(lista[0]) == dict:
            # cabecera tabla
            tabla = """
            <table
            data-toggle="table"
            data-search="true"
            data-show-columns="true"
            data-show-fullscreen="true"
            data-locale="es-AR"
            data-classes = "table table-bordered table-hover table-sm"
            > <thead> <tr>"""

            for i in claves:
                tabla = tabla + '<th data-field="%s" data-sortable="true">%s</th>' % (i, i)
            tabla = tabla + '</tr> </thead> <tbody>'
            # contenido tabla
            for i in lista:
                tabla = tabla + '<tr>'
                for j in claves:
                    tabla = tabla + '<td>%s</td>' % (i[j])
                tabla = tabla + '</tr>'
            tabla = tabla + '</tbody> </table>'
            cantidad = len(lista)
            leyenda_cantidad = MARKMIN("Cantidad de registros: " + str(cantidad))
            if nombre_archivo == 'mov_caja':
                directorio = f'{files_dir}mov_caja/'
            session.nombre_archivo = list_of_dict_to_csv(
                nombre_archivo, lista, dir=directorio)[1]
            # open_archivo = open('applications/' + str(configuration.get('app.name')) + '/files/csv/'+session.nombre_archivo, "r")
            boton_csv = A('Descarga tabla como CSV...',
                          _href=URL('tapa14', 'default', 'descarga_csv'),
                          _class='btn btn-default')
            # return CENTER(TABLE(boton_csv,XML(tabla)))
            return DIV(XML(tabla), leyenda_cantidad, boton_csv)


def list_dict_to_table_sortable1(lista, nombre_archivo, claves):
    '''recibe una lista de diccionarios(clave-valor iguales) y
     devuelve una tabla html'''
    if type(lista) == list:
        if type(lista[0]) == dict:
            # cabecera tabla
            tabla = '<table data-toggle="table"> <thead> <tr>'
            for i in claves:
                tabla = tabla + '<th data-field="%s" data-sortable="true">%s</th>' % (i, i)
            tabla = tabla + '</tr> </thead> <tbody>'
            # contenido tabla
            for i in lista:
                tabla = tabla + '<tr>'
                for j in claves:
                    tabla = tabla + '<td>%s</td>' % (i[j])
                tabla = tabla + '</tr>'
            tabla = tabla + '</tbody> </table>'
            cantidad = len(lista)
            leyenda_cantidad = MARKMIN("Cantidad de registros: " + str(cantidad))
            session.nombre_archivo = list_of_dict_to_csv(nombre_archivo, lista)[1]
            # open_archivo = open('applications/' + str(configuration.get('app.name')) + '/files/csv/'+session.nombre_archivo, "r")
            boton_csv = A('Descarga tabla como CSV...',
                          _href=URL('tapa14', 'default', 'descarga_csv'),
                          _class='btn btn-default')
            # return CENTER(TABLE(boton_csv,XML(tabla)))
            return DIV(XML(tabla), leyenda_cantidad, boton_csv)


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
