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
    # from util_afip import *  # funciones de pyafipws
    # from info_afip import *  # datos de pyafipws


# "Fecha","Tipo","Punto de Venta","Número Desde","Número Hasta",
# "Cód. Autorización","Tipo Doc. Receptor","Nro. Doc. Receptor",
# "Denominación Receptor","Tipo Cambio", "Moneda","Imp. Neto Gravado",
# "Imp. Neto No Gravado","Imp. Op. Exentas","IVA","Imp. Total"

# modelo cabecera, alicuotas, ventas, detalle

# defino clave para documentos, compuesto por
# reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"]
# (completado los zeros)


def registros_id(tuple):
    tipo_cbte_size = 3
    punto_vta_size = 5
    cbt_numero_size = 20
    salida = (str(tuple[0]).zfill(tipo_cbte_size) +
              str(tuple[1]).zfill(punto_vta_size) +
              str(tuple[1]).zfill(cbt_numero_size))
    return(salida)


formato_decimal = 'decimal(25,2)'


# corresponde a ALICUOTAS: REGINFO_CV_VENTAS_CBTE_ALICUOTA, 63
db.define_table(
    'cbte_alicuotas',
    Field('comprobante', 'string', unique=True),
    Field('tipo_cbte', 'integer'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('base_imp', formato_decimal),
    Field('iva_id', 'integer'),
    Field('importe', formato_decimal),
    Field('fecha_carga', 'datetime'),
    Field('fecha_mod', 'datetime'),
    format='%(comprobante)s'
)

# corresponde VENTAS: REGINFO_CV_VENTAS_CBTE_NUEVO, 267
db.define_table(
    'cbte_ventas',
    Field('comprobante', 'string', unique=True),
    Field('fecha_cbte', 'datetime'),
    Field('tipo_cbte', 'integer'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('cbte_nro_reg', 'integer'),
    Field('tipo_doc', 'integer'),
    Field('nro_doc', 'integer'),
    Field('nombre', 'string'),
    Field('imp_total', formato_decimal),
    Field('imp_tot_conc', formato_decimal),
    Field('impto_liq_rni', formato_decimal),
    Field('imp_op_ex', formato_decimal),
    Field('impto_perc', formato_decimal),
    Field('imp_iibb', formato_decimal),
    Field('impto_perc_mun', formato_decimal),
    Field('imp_internos', formato_decimal),
    Field('moneda_id', 'integer'),
    Field('moneda_ctz', formato_decimal),
    Field('cant_alicuota_iva', 'integer'),
    Field('codigo_operacion', 'string'),
    Field('imp_trib', formato_decimal),
    Field('fecha_venc_pago', 'datetime'),
    Field('fecha_carga', 'datetime'),
    Field('fecha_mod', 'datetime'),
    format='%(comprobante)s'
)

# corresponde CABECERA: CAB_FAC_TIPO1, 291
db.define_table(
    'cbte_cabecera',
    Field('comprobante', 'string'),
    Field('tipo_reg', 'integer'),
    Field('fecha_cbte', 'datetime'),
    Field('tipo_cbte', 'integer'),
    Field('ctl_fiscal', 'string'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('cbte_nro_reg', 'integer'),
    Field('cant_hojas', 'integer'),
    Field('tipo_doc', 'integer'),
    Field('nro_doc', 'integer'),
    Field('nombre', 'string'),
    Field('imp_total', formato_decimal),
    Field('imp_tot_conc', formato_decimal),
    Field('imp_neto', formato_decimal),
    Field('impto_liq', formato_decimal),
    Field('impto_liq_rni', formato_decimal),
    Field('imp_op_ex', formato_decimal),
    Field('impto_perc', formato_decimal),
    Field('imp_iibb', formato_decimal),
    Field('impto_perc_mun', formato_decimal),
    Field('imp_internos', formato_decimal),
    Field('transporte', formato_decimal),
    Field('categoria', 'integer'),
    Field('imp_moneda_id', 'string'),
    Field('imp_moneda_ctz', formato_decimal),
    Field('alicuotas_iva', 'integer'),
    Field('codigo_operacion', 'string'),
    Field('cae', 'integer'),
    Field('fecha_vto', 'datetime'),
    Field('fecha_anulacion', 'datetime'),
    Field('fecha_carga', 'datetime'),
    Field('fecha_mod', 'datetime'),
)


# corresponde DETALLE: DETALLE_TIPO1, 190
db.define_table(
    'cbte_detalle',
    Field('comprobante', 'string', unique=True),
    Field('tipo_cbte', 'integer'),
    Field('ctl_fiscal', 'string'),
    Field('fecha_cbte', 'datetime'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('cbte_nro_reg', 'integer'),
    Field('cantidad', 'integer'),
    Field('xxx1', 'string'),
    Field('pro_umed', 'string'),
    Field('pro_precio_uni', formato_decimal),
    Field('imp_bonif', formato_decimal),
    Field('imp_ajuste', formato_decimal),
    Field('imp_total', formato_decimal),
    Field('alicuota_iva', formato_decimal),
    Field('gravado', 'string'),
    Field('anulacion', 'string'),
    Field('cyd', 'string'),
    Field('fecha_carga', 'datetime'),
    Field('fecha_mod', 'datetime'),
    format='%(comprobante)s'
)


def ingreso_cbtes(tipo, cbtes_dict):
    # tipos alicuotas, ventas, cabecera, detalle
    if type(cbtes_dict) != dict:
        return ['error', '']
    if tipo == 'alicuotas':
        for i in cbtes_dict.keys():
            pass


def test_ingreso_cabecera():
    t_procesos = test_proceso_REGISTRO()
    # registro: 0 cabecera, 1 ventas, 2 alicuotas, 3 detalle
    registro = (0, 'cabecera')
    registro = (1, 'ventas')
    registro = (2, 'alicuotas')
    registro = (3, 'detalle')
    k_procesos = t_procesos[registro][1].keys()
    for key in k_procesos:
        t_procesos[registro][1][key]['comprobante'] = str(key)
        t_procesos[registro][1][key]['fecha_carga'] = datetime.datetime.now()
        t_procesos[registro][1][key]['fecha_mod'] = datetime.datetime.now()
        db['cbte_cabecera'].insert(**t_procesos[0][1][key])
    # a[0][1][(1, 4, 3892)]['fecha_carga'] = datetime.datetime.now()
    # a[0][1][(1, 4, 3892)][''] = datetime.datetime.now()
    # db['cbte_cabecera'].insert(**a[0][1][(1, 4, 3892)]) 
    db.commit()


def proceso_REGISTRO(ARCHIVO, tipo):
    tiporeg = TIPOS_REGISTROS[tipo][0]
    cantreg = TIPOS_REGISTROS[tipo][1]
    procesado = {}
    try:
        for linea in open(ARCHIVO, 'r', encoding='latin1'):
            if len(linea) == cantreg:
                reg = leer(linea, eval(tiporeg))
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
    cabecera = proceso_REGISTRO(path + 'CABECERA.txt', 'CABECERA')
    ventas = proceso_REGISTRO(path + 'VENTAS.txt', 'VENTAS')
    alicuotas = proceso_REGISTRO(path + 'ALICUOTAS.txt', 'ALICUOTAS')
    detalle = proceso_REGISTRO(path + 'DETALLE.txt', 'DETALLE')
    return cabecera, ventas, alicuotas, detalle
