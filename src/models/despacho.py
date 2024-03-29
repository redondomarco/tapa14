# -*- coding: utf-8 -*-
"""
Funciones referidas al despacho

"""
import random
import datetime
from pyexcel_ods3 import get_data


# for ide
if 1 == 2:
    # from gluon import
    from db import log, db
    from util import files_dir
    from pdf import base_dir, analizo_fa
    from os import walk


def mapeo_prod(producto):
    """ identifico productos de listados externos para el sistema"""
    minus = str(producto).lower()
    if 'LM_DISCOS_FREIR_123_x_12'.lower() in minus:
        return [producto, 'LM123DC']
    if 'LM_DISCOS_HORNO_123_x_12'.lower() in minus:
        return [producto, 'LM123DH']
    if 'LM_PASCUALINA_HOJALDRE_300_x_2'.lower() in minus:
        return [producto, 'LM300PH']
    if 'SRR_DISCOS_FREIR_123_x_12_x18u'.lower() in minus:
        return [producto, 'SRR123DC']
    if 'SRR_DISCOS_HORNO_123_x_12_x18u'.lower() in minus:
        return [producto, 'SRR123DH']
    if 'SRR_PASCUALINA_HOJALDRE_300_x_2x16u'.lower() in minus:
        return [producto, 'SRR300PH']
    if 'PNN_DISCOS_FREIR_123_x_12'.lower() in minus:
        return [producto, 'PNN123DC']
    if 'PNN_DISCOS_HORNO_123_x_12'.lower() in minus:
        return [producto, 'PNN123DH']
    if 'PNN_PASCUALINAS_HORNO_123_x_12'.lower() in minus:
        return [producto, 'PNN300PH']
    # dc
    if all(['empanada' in minus,
            'criolla' in minus,
            '123' in minus,
            '18' in minus]):
        return [producto, 'TDC123x18']
    # dh
    elif all(['empanada' in minus,
              'hojaldre' in minus,
              '123' in minus,
              '18' in minus]):
        return [producto, 'TDH123x18']
    # pc
    elif all(['pascualina' in minus,
              'criolla' in minus,
              '300' in minus,
              '16' in minus]):
        return [producto, 'TPC300x16']
    # variante pc
    elif all(['pascualina' in minus,
              'criolla' in minus,
              '300' in minus]):
        return [producto, 'TPC300x16']
    # variante pc 1
    elif all(['pc' in minus,
              '300' in minus]):
        return [producto, 'TPC300x16']
    # ph
    elif all(['pascualina' in minus,
              'hojaldre' in minus,
              '300' in minus,
              '16' in minus]):
        return [producto, 'TPH300x16']
    # rc
    elif all(['rotisero' in minus,
              'criollo' in minus,
              '135' in minus,
              '12' in minus]):
        return [producto, 'TRC135x12']
    # rh
    elif all(['rotisero' in minus,
              'hojaldre' in minus,
              '135' in minus,
              '12' in minus]):
        return [producto, 'TRH135x12']
    # rc135 cat
    elif all(['rotisero' in minus,
              'criollo' in minus,
              '135' in minus]):
        return [producto, 'TRC135xDOC']
    # rc135 cat
    elif all(['rotisero' in minus,
              'criollo' in minus,
              'xc' in minus,
              '160' in minus]):
        return [producto, 'TRC160xDOC']
    # rh147 cat
    elif all(['super' in minus,
              'rotisero' in minus,
              '147' in minus]):
        return [producto, 'TRH147xDOC']
    # rh160 cat
    elif all(['rotisero' in minus,
              'hojaldre' in minus,
              '160' in minus]):
        return [producto, 'TRH160xDOC']

    # minit
    elif all(['mini' in minus, 'hojaldre' in minus, '220' in minus]):
        return [producto, 'MTH220']

    # copetin varios
    elif all(['copetin' in minus, 'criollo' in minus]):
        return [producto, 'TDC123x18']
        # return [producto,'TCHxDOC']
    elif all(['copetin' in minus, 'criollo' in minus]):
        return [producto, 'TDC123x18']
        # return [producto,'TCHxDOC']

    # errores granbai
    elif any(['dow' in minus,
              'jd' in minus,
              'cp' in minus,
              'deere' in minus,
              'rotiser/o' in minus,
              'em/panada' in minus,
              'camioneros' in minus,
              'tapa_empanada_criolla' in minus]):
        return [producto, 'TRH135x12']

    # lm
    elif all(['disco' in minus,
              'criollo' in minus,
              '123' in minus,
              '12' in minus,
              '20' in minus]):
        return [producto, 'LM123DC']
    elif all(['disco' in minus,
              'hojaldre' in minus,
              '123' in minus,
              '12' in minus,
              '20' in minus]):
        return [producto, 'LM123DH']
    # lm PH
    elif all(['pascualina' in minus,
              'hojaldre' in minus,
              '300x2x20' in minus]):
        return [producto, 'LM300PH']
    # panin
    elif all(['discos' in minus,
              'freir' in minus,
              '123' in minus,
              '12' in minus]):
        # log(producto)
        return [producto, 'PNN123DC']
    elif all(['discos' in minus,
              'horno' in minus,
              '123' in minus,
              '12' in minus]):
        return [producto, 'PNN123DH']
    elif all(['pascualina' in minus,
              'criolla' in minus,
              '300' in minus,
              '2' in minus]):
        return [producto, 'PNN300PC']
    elif all(['pascualina' in minus,
              'hojaldre' in minus,
              '300' in minus,
              '2' in minus]):
        return [producto, 'PNN300PH']

    # sin etiqueta
    else:
        log(str(producto) + ' sin etiqueta')
        return[producto, producto]


def busca_lote(fechaf, producto):
    lotes = []
    # fechafa = datetime.strptime(fechaf, '%d/%m/%Y')
    fechafa = fechaf
    # un_csv = '/csv/elaboracion/elab_1-04-208_al_7-11-2018.csv'
    # un_csv = '/csv/elaboracion/elab_1-6-2019_al_30-11-2019.csv'
    # un_csv = '/csv/elaboracion/elab_1-11-2021_al_16-05-2022.csv'
    un_csv = '/csv/elaboracion/todos.csv'
    csvleido = open(base_dir + un_csv, 'r').read().split()
    lista = []
    # formateo csv
    for i in csvleido:
        aux = i.split(',')
        # log(aux)
        fecha = datetime.datetime.strptime(aux[0], '%Y/%m/%d')
        prod = aux[1]
        lote = aux[2]
        lista.append([fecha, prod, lote])
    # return lista
    n = 1
    while lotes == []:
        lotes = sub_busca_lote(lista, n, producto, fechafa)
        n += 1
        if n == 30:
            # busco en n+ dias
            lotes = sub_busca_lote_post(lista, 7, producto, fechafa)
            #
            if lotes == []:
                log('algo esta mal ' + str(fechaf) + str(producto))
                break
    return list(set(lotes))


def sub_busca_lote(lista, dias, producto, fechafa):
    lotes = []
    for i in lista:
        if i[1] == producto:
            # si la fecha de elboracion es X dias o menos de la
            # fecha de la factura lo agrego
            if all([i[0] >= (fechafa - datetime.timedelta(days=dias)),
                    i[0] <= fechafa]):
                lotes.append(i[2])
    return lotes


def sub_busca_lote_post(lista, dias, producto, fechafa):
    lotes = []
    for i in lista:
        if i[1] == producto:
            # si la fecha de elboracion es X dias o menos de la
            # fecha de la factura lo agrego
            if all([i[0] >= (fechafa),
                    i[0] <= fechafa + datetime.timedelta(days=dias)]):
                lotes.append(i[2])
    return lotes


# funcion antigua para leer facturas pdf
def leo_para_despacho():
    dir, subdirs, archivos = next(walk('applications/dev/files/facturas/'))
    resultado = []
    for factura in archivos:
        # log('analizo: '+dir+factura)
        fleida = analizo_fa(dir + factura)
        if fleida[0] == 'error':
            # log('error con factura: '+str(factura))
            pass
        else:
            for articulo in fleida[1]['d_art']:
                producto = mapeo_prod(articulo[1])[1]
                fecha = fleida[1]['f_fechae']
                lote = busca_lote(fecha, producto)
                aux = {
                    'producto': producto,
                    'cant': articulo[2],
                    'fa_n': fleida[1]['f_nro'],
                    'fecha': fleida[1]['f_fechae'],
                    'cliente': fleida[1]['r_rsocial'],
                    'lote': lote,
                    # 'md5':fleida[1]['md5'],
                    # 'nota':fleida[1]['nota']
                }
                resultado.append(aux)
            # resultado.append(fleida[1])
    log('fin proceso leer facturas')
    return resultado


def proceso_detalle_despacho():
    # busco registros detalle de facturacion
    # entre fechas
    fecha_inicio = datetime.datetime(2021, 11, 1, 0, 0)
    fecha_fin = datetime.datetime(2022, 5, 16, 0, 0)
    cons = db((db.cbte_DETALLE.fecha_cbte >= fecha_inicio) and
              (db.cbte_DETALLE.fecha_cbte <= fecha_fin)).select()
    registros = cons.as_dict()
    # return registros
    clienteold = ''
    resultado = []
    for i in registros.keys():
        cyd = registros[i]['cyd']
        if descarto_productos_despacho(cyd):
            producto = mapeo_prod(cyd)[1]
            comprobante = registros[i]['comprobante'][0:28]
            # log(comprobante)
            try:
                selec_cbte = (db.cbte_CABECERA.comprobante == comprobante)
                cons1 = db(selec_cbte).select()
                cliente = cons1.first().as_dict()['nombre']
                # logica para mismo cliente mismo vehiculo
                if clienteold != cliente:
                    # hace random el nuevo vehiculo
                    vehiculo = random.choice(['Lifan_1', 'Shineray_1', 'Shineray_2'])
                else:
                    # queda el mismo vehiculo
                    pass
                clienteold = cliente
                fecha = registros[i]['fecha_cbte']
                aux = {
                    'producto': str(producto),
                    'cantidad': str(registros[i]['cantidad']),
                    'fa_n': 'fa-' + str(comprobante),
                    'fecha': fecha.date(),
                    'cliente': str(cliente),
                    'lote': str(busca_lote(fecha, producto)),
                    'responsable': 'RAMON',
                    'vehiculo': vehiculo
                }
                resultado.append(aux)
            except Exception as e:
                log(comprobante)
                log(e)
        else:
            pass
            # log('descartado ' + str(producto))
    # en cada registro:
    # identifico producto
    # determino cantidad
    # fecha facturacion
    # lote de acuerdo a la fecha y producto
    log('fin proceso analizar despacho')
    return resultado


def descarto_productos_despacho(producto):
    minus = str(producto).lower()
    if any(['mth220' in minus,
            'mini_tarta' in minus,
            'empresarial' in minus,
            'devolucion' in minus,
            'diferencia' in minus,
            'logistica' in minus,
            'logística' in minus,
            'correcci' in minus,
            'cheque' in minus,
            'bancario' in minus,
            'oquis' in minus,
            'ravioles' in minus,
            'tallarine' in minus,
            'fideo' in minus,
            'cajas de discos' in minus,
            'mezcladora' in minus]):
        return False
    else:
        return True


def leo_elaboracion():
    dir_elab = 'elaboracion/'
    file_elab = 'REGISTRO ELABORACION Y ENVASADO.ods'
    archivo_elaboracion = files_dir + dir_elab + file_elab
    data = get_data(archivo_elaboracion)
    return data


def compilo_elaboracion():
    planilla = leo_elaboracion()
    compilado = []
    # for hoja in planilla.keys():
