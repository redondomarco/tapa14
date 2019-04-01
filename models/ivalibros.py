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


def proceso_archivos(VENTAS, ALICUOTAS,
                     CABECERA, DETALLE):
    ops = {}
    for linea in open(CABECERA, 'r', encoding='latin1'):
        log(len(linea))
        reg = leer(linea, CAB_FAC_TIPO1)
        key = (reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"])
        if key != (0, 0, 0):
            ops[key] = reg
            # log(key)
    # alicuotas
    for linea in open(ALICUOTAS, 'r', encoding='latin1'):
        iva = leer(linea, REGINFO_CV_VENTAS_CBTE_ALICUOTA)
        key = (iva["tipo_cbte"], iva["punto_vta"], iva["cbt_numero"])
        reg = ops[key]
        reg["imp_neto"] = reg.get("imp_neto", 0.00) + iva["base_imp"]
        reg["imp_iva"] = reg.get("imp_iva", 0.00) + iva["importe"]
        reg.setdefault("iva", []).append(iva)
    # ventas
    #for linea in open(VENTAS, 'r', encoding='latin1'):
    #    iva = leer(linea, REGINFO_CV_VENTAS_CBTE_ALICUOTA)
    #    key = (iva["tipo_cbte"], iva["punto_vta"], iva["cbt_numero"])
    #    reg = ops[key]
    #    reg["imp_neto"] = reg.get("imp_neto", 0.00) + iva["base_imp"]
    #    reg["imp_iva"] = reg.get("imp_iva", 0.00) + iva["importe"]
    #    reg.setdefault("iva", []).append(iva)
    # detalle

#    facts = sorted(ops.values(), key=lambda f: (
#        f["tipo_cbte"], f["punto_vta"], f["cbt_numero"])) 
    return ops


def test_proceso_archivos():
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/')
    return proceso_archivos(path + 'VENTAS.txt',
                            path + 'ALICUOTAS.txt',
                            path + 'CABECERA.txt',
                            path + 'DETALLE.txt',
                            )
