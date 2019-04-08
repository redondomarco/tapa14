# -*- coding: utf-8 -*-
#
# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    from db import *
    from util import *
    #from util_afip import *  # funciones de pyafipws
    #from info_afip import *  # datos de pyafipws


# "Fecha","Tipo","Punto de Venta","Número Desde","Número Hasta",
# "Cód. Autorización","Tipo Doc. Receptor","Nro. Doc. Receptor",
# "Denominación Receptor","Tipo Cambio", "Moneda","Imp. Neto Gravado",
# "Imp. Neto No Gravado","Imp. Op. Exentas","IVA","Imp. Total"


def proceso_REGISTRO(ARCHIVO, tipo):
    tiporeg = TIPOS_REGISTROS[tipo][0]
    cantreg = TIPOS_REGISTROS[tipo][1]
    procesado = {}
    try:
        for linea in open(ARCHIVO, 'r', encoding='latin1'):
            if len(linea) == cantreg:
                reg = leer(linea, tiporeg)
                key = (reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"])
                procesado[key] = reg
            else:
                mensaje = "Error en longitud de la linea %s , %s" % (
                    linea, len(linea))
                log(mensaje)
        return ['ok', procesado]
    except Exception as e:
        mensaje = 'Error: ' + str(e)
        log(mensaje)
        return ['error', mensaje]

def test_proceso_REGISTRO():
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/')
    cabecera=proceso_REGISTRO(path + 'CABECERA.txt', 'CABECERA')
    return cabecera

def proceso_CAB_FAC_TIPO1(CABECERA):
    cabecera = {}
    try:
        for linea in open(CABECERA, 'r', encoding='latin1'):
            if len(linea) == 291:
                reg = leer(linea, CAB_FAC_TIPO1)
                key = (reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"])
                cabecera[key] = reg
            else:
                mensaje = "Error en longitud de la linea %s , %s" % (
                    linea, len(linea))
                log(mensaje)
        return ['ok', cabecera]
    except Exception as e:
        mensaje = 'Error: ' + str(e)
        log(mensaje)
        return ['error', mensaje]


def proceso_REGINFO_CV_VENTAS_CBTE_ALICUOTA(ALICUOTAS):
    alicuotas = {}
    try:
        for linea in open(ALICUOTAS, 'r', encoding='latin1'):
            if len(linea) == 63:
                reg = leer(linea, REGINFO_CV_VENTAS_CBTE_ALICUOTA)
                key = (iva["tipo_cbte"], iva["punto_vta"], iva["cbt_numero"])
                alicuotas[key] = reg
            else:
                mensaje = "Error en longitud de la linea %s , %s" % (
                    linea, len(linea))
                log(mensaje)
        return['ok', alicuotas]
    except Exception as e:
        mensaje = 'Error: ' + str(e)
        log(mensaje)
        return ['error', mensaje]


def proceso_REGINFO_CV_VENTAS_CBTE_NUEVO(VENTAS):
    ventas = {}
    try:
        for linea in open(VENTAS, 'r', encoding='latin1'):
            if len(linea) == 266:
                reg = leer(linea, REGINFO_CV_VENTAS_CBTE_NUEVO)
                key = (iva["tipo_cbte"], iva["punto_vta"], iva["cbt_numero"])
                ventas[key] = reg
            else:
                mensaje = "Error en longitud de la linea %s , %s" % (
                    linea, len(linea))
                log(mensaje)
        return['ok', ventas]
    except Exception as e:
        mensaje = 'Error: ' + str(e)
        log(mensaje)
        return ['error', mensaje]






def test_proceso_archivos():
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/')
    return proceso_archivos(path + 'VENTAS.txt',
                            path + 'ALICUOTAS.txt',
                            path + 'CABECERA.txt',
                            path + 'DETALLE.txt',
                            )


def test_proceso_individual(archivo):
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/')
    filepath = path + archivo
    ops = {}
    for linea in open(filepath, 'r', encoding='latin1'):
        lectura = leer(linea, REGINFO_CV_VENTAS_CBTE_NUEVO)
        key = (reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"])
        ops[key] = reg
    return ops
