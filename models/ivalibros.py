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

# db.define_table(
#    'fact_a_emitidas',
#    Field)


def proceso_archivos(VENTAS, ALICUOTAS,
                     CABECERA, DETALLE):
    ops = {}

    for linea in open(CABECERA, 'r', encoding='latin1'):
        log(linea)
        log(linea)

        reg = leer(linea, REGINFO_CV_VENTAS_CBTE)
        reg["cae"] = ""  # no uso cae anticipado
        reg["concepto"] = 1  # siempre es producto
        if concepto == 2:
            reg["fecha_serv_desde"] = fecha_serv_desde
            reg["fecha_serv_hasta"] = fecha_serv_hasta
        else:
            del reg['fecha_venc_pago']
        key = (reg["tipo_cbte"], reg["punto_vta"], reg["cbt_desde"])
        ops[key] = reg
        log(key)

    for linea in open("ALI.txt", 'r', encoding='latin1'):
        iva = leer(linea, REGINFO_CV_VENTAS_CBTE_ALICUOTA)
        key = (iva["tipo_cbte"], iva["punto_vta"], iva["cbt_numero"])
        reg = ops[key]
        reg["imp_neto"] = reg.get("imp_neto", 0.00) + iva["base_imp"]
        reg["imp_iva"] = reg.get("imp_iva", 0.00) + iva["importe"]
        reg.setdefault("iva", []).append(iva)
    facts = sorted(ops.values(), key=lambda f: (
        f["tipo_cbte"], f["punto_vta"], f["cbt_desde"]))
    return facts, ops


def test_proceso_archivos():
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/')
    proceso_archivos(path + 'VENTAS.txt',
                     path + 'ALICUOTAS.txt',
                     path + 'CABECERA.txt',
                     path + 'DETALLE.txt',
                     )
