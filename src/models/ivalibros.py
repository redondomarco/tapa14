# -*- coding: utf-8 -*-
#
import hashlib
# for ide
if 1 == 2:
    from gluon import Field
    from db import db, configuration
    import datetime
    from log import log
    from info_afip import TIPOS_REGISTROS
    from util_afip import leer
    from util import todos_los_archivos, files_dir


# "Fecha","Tipo","Punto de Venta","Número Desde","Número Hasta",
# "Cód. Autorización","Tipo Doc. Receptor","Nro. Doc. Receptor",
# "Denominación Receptor","Tipo Cambio", "Moneda","Imp. Neto Gravado",
# "Imp. Neto No Gravado","Imp. Op. Exentas","IVA","Imp. Total"

# modelo cabecera, alicuotas, ventas, detalle

# defino clave para documentos, compuesto por
# reg["tipo_cbte"], reg["punto_vta"], reg["cbt_numero"]
# (completado los zeros)


def registros_id(lista):
    tipo_cbte_size = 3
    punto_vta_size = 5
    cbt_numero_size = 20
    salida = (str(lista[0]).zfill(tipo_cbte_size) +
              str(lista[1]).zfill(punto_vta_size) +
              str(lista[2]).zfill(cbt_numero_size))
    return(salida)


formato_decimal = 'decimal(25,2)'


def detalle_id(lista, cyd):
    m = hashlib.md5()
    m.update(cyd.encode('utf-8'))
    salida = registros_id(lista) + m.hexdigest()
    return salida


def test_detalle_id():
    a = id_detalle([0, 1, 2], 'detalle')
    if a == '0000000100000000000000000002f019564bfcfa0a562d25341e83ca087b':
        return True


# corresponde a ALICUOTAS: REGINFO_CV_VENTAS_CBTE_ALICUOTA, 63
db.define_table(
    'cbte_ALICUOTAS',
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
    'cbte_VENTAS',
    Field('comprobante', 'string', unique=True),
    Field('fecha_cbte', 'datetime'),
    Field('tipo_cbte', 'integer'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('cbte_nro_reg', 'integer'),
    Field('tipo_doc', 'integer'),
    Field('nro_doc', 'string'),
    Field('nombre', 'string'),
    Field('imp_total', formato_decimal),
    Field('imp_tot_conc', formato_decimal),
    Field('impto_liq_rni', formato_decimal),
    Field('imp_op_ex', formato_decimal),
    Field('impto_perc', formato_decimal),
    Field('imp_iibb', formato_decimal),
    Field('impto_perc_mun', formato_decimal),
    Field('imp_internos', formato_decimal),
    Field('moneda_id', 'string'),
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
    'cbte_CABECERA',
    Field('comprobante', 'string', unique=True),
    Field('tipo_reg', 'integer'),
    Field('fecha_cbte', 'datetime'),
    Field('tipo_cbte', 'integer'),
    Field('ctl_fiscal', 'string'),
    Field('punto_vta', 'integer'),
    Field('cbt_numero', 'integer'),
    Field('cbte_nro_reg', 'integer'),
    Field('cant_hojas', 'integer'),
    Field('tipo_doc', 'integer'),
    Field('nro_doc', 'string'),
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
    Field('cae', 'string'),
    Field('fecha_vto', 'datetime'),
    Field('fecha_anulacion', 'datetime'),
    Field('fecha_carga', 'datetime'),
    Field('fecha_mod', 'datetime'),
)


# corresponde DETALLE: DETALLE_TIPO1, 190
db.define_table(
    'cbte_DETALLE',
    Field('comprobante', 'string'),
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


def dev_ingreso_cabecera():
    t_procesos = test_proceso_REGISTRO()
    # registro: 0 cabecera, 1 ventas, 2 alicuotas, 3 detalle
    registro = {0: 'CABECERA',
                1: 'VENTAS',
                2: 'ALICUOTAS',
                3: 'DETALLE'
                }
    actual = 0
    k_procesos = t_procesos[actual][1].keys()
    for key in k_procesos:
        hoy = datetime.datetime.now()
        if db(db.cbte_cabecera.comprobante == str(key)).select().first():
            # ya existe lo actualizo
            t_procesos[actual][1][key]['fecha_mod'] = hoy
            # log(str(t_procesos[actual][1][key]['fecha_mod']))
            # log('actualizo ' + str(key))
            db(db['cbte_' + registro[actual]].comprobante == str(key)).update(
                **t_procesos[actual][1][key])
            # log(a)
            # return t_procesos[0][1][key]
        else:
            t_procesos[registro][1][key]['comprobante'] = str(key)
            t_procesos[registro][1][key]['fecha_carga'] = hoy
            t_procesos[registro][1][key]['fecha_mod'] = hoy
            db['cbte_cabecera'].insert(**t_procesos[0][1][key])
    # a[0][1][(1, 4, 3892)]['fecha_carga'] = datetime.datetime.now()
    # a[0][1][(1, 4, 3892)][''] = datetime.datetime.now()
    # db['cbte_cabecera'].insert(**a[0][1][(1, 4, 3892)])
    db.commit()


def subo_cbtes(ARCHIVO):
    hoy = datetime.datetime.now()
    # determino tipo
    tipo = identifico_registro(ARCHIVO)
    if tipo[0] == 'ok':
        log('proceso archivo tipo: ' + str(tipo[1]))
        nombre_cbte = 'cbte_' + str(tipo[1])
        t_procesos = proceso_REGISTRO(ARCHIVO)
        reg_updates = []
        reg_inserts = []
        if t_procesos[0] == 'ok':
            k_procesos = t_procesos[1].keys()
            for key in k_procesos:
                selector = 'db.' + nombre_cbte + '.comprobante'
                # log('key: ' + str(key) + ' selector' + str(selector))
                if db(eval(selector) == str(key)).select().first():
                    t_procesos[1][key]['fecha_mod'] = hoy
                    db(db[nombre_cbte].comprobante == str(key)).update(
                        **t_procesos[1][key])
                    reg_updates.append(key)
                else:
                    t_procesos[1][key]['comprobante'] = str(key)
                    t_procesos[1][key]['fecha_carga'] = hoy
                    t_procesos[1][key]['fecha_mod'] = hoy
                    log(str(t_procesos[1][key]))
                    try:
                        db[nombre_cbte].insert(**t_procesos[1][key])
                        reg_inserts.append(key)
                    except Exception as e:
                        log('problema con: ' + str(t_procesos[1][key]) +
                            ' e: ' + str(e))
            db.commit()
            mensaje = (str(len(reg_updates)) + ' registros actualizados: ' +
                       str(len(reg_inserts)) + ' registros agregados')
            log(mensaje)
            return ['ok', mensaje]
        else:
            log('error t-procesos')
            return t_procesos
    else:
        log('error tipo')
        return tipo


def test_subo_cbtes():
    archivos = [
        'applications/tapa14/files/VENTAS.txt',
        'applications/tapa14/files/VENTAS1.txt',
        'applications/tapa14/files/ALICUOTAS.txt',
        'applications/tapa14/files/ALICUOTAS1.txt',
        'applications/tapa14/files/DETALLE.txt',
        'applications/tapa14/files/DETALLE1.txt',
        'applications/tapa14/files/CABECERA.txt',
        'applications/tapa14/files/CABECERA1.txt',
    ]
    resultados = []
    for archivo in archivos:
        log('intento subir cbte: ' + str(archivo))
        resultados.append(subo_cbtes(archivo))
    return resultados


def identifico_registro(ARCHIVO):
    """segun longitud de la linea determino el tipo de archivo afip"""
    try:
        for linea in open(ARCHIVO, 'r', encoding='latin1'):
            longitud = len(linea)
            for tipo in TIPOS_REGISTROS.keys():
                if TIPOS_REGISTROS[tipo][1] == longitud:
                    return ['ok', tipo]
            # si llego aca es que no correponde a ningun tipo conocido
            return ['error', 'la longitud no corresponde a ningun tipo']
    except Exception as e:
        mensaje = ['error', str(e)]
        log(mensaje)
        return mensaje


def proceso_REGISTRO(ARCHIVO):
    """ proceso archivo de afip y lo convierto en un diccionario"""
    tipo = identifico_registro(ARCHIVO)
    if tipo[0] == 'ok':
        log('proceso archivo tipo: ' + str(tipo[1]))
        tiporeg = TIPOS_REGISTROS[tipo[1]][0]
        cantreg = TIPOS_REGISTROS[tipo[1]][1]
    else:
        return tipo
    procesado = {}
    try:
        for linea in open(ARCHIVO, 'r', encoding='latin1'):
            if len(linea) == cantreg:
                reg = leer(linea, eval(tiporeg))
                cbte = [reg["tipo_cbte"],
                        reg["punto_vta"],
                        reg["cbt_numero"]]
                if tipo[1] == 'DETALLE':
                    key = detalle_id(cbte, reg['cyd'])
                else:
                    key = registros_id(cbte)
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
    cabecera = proceso_REGISTRO(path + 'CABECERA.txt')
    ventas = proceso_REGISTRO(path + 'VENTAS.txt')
    alicuotas = proceso_REGISTRO(path + 'ALICUOTAS.txt')
    detalle = proceso_REGISTRO(path + 'DETALLE.txt')
    return cabecera, ventas, alicuotas, detalle


def subo_registros_batch():
    archivos = todos_los_archivos(files_dir + 'facturacion')
    for archivo in archivos:
        subo_cbtes(archivo)

