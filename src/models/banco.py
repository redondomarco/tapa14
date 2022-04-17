# -*- coding: utf-8 -*-
import pandas as pd
# for ide
if 1 == 2:
    import datetime
    from log import log
    from cajas import id_cajas
    from modelo import db


def proceso_xls_coinag(archivo):
    df = pd.read_excel(io=archivo)
    # saco hora 00:00:00
    fecha = 'Fecha / Hora Mov.'
    df[fecha] = df[fecha].map(lambda x: x.split(' ')[0])
    # borro columna
    del df['Comentarios']
    # agrego columna id
    return df


def test_proceso_xls_coinag():
    path = 'applications/tapa14/files/upload/2020-12-4/'
    file = '2020-12-4_LaBM_COINAG_2020_10.xls'
    return proceso_xls_coinag(path + file)


def operaciones_ids():
    resultado = []
    ids = db(db.caja).select(db.caja.id, db.caja.operacionid)
    for i in ids:
        resultado.append(i.operacionid)
    return resultado


def insert_xls_coinag(archivo):
    registros = proceso_xls_coinag(archivo).to_dict(orient='index')
    idoperaciones = operaciones_ids()
    duplicadas = []
    insertado = 0
    for row in registros:
        f_leida = registros[row]['Fecha / Hora Mov.']
        fecha = datetime.datetime.strptime(f_leida, '%d/%m/%Y')
        concepto = registros[row]['Concepto']
        importe = float(registros[row]['Importe'])
        id_registro = id_cajas(fecha,
                               concepto,
                               importe)
        # log(f'inserto {registros[row]} id {id_registro}')
        # determino si es ingreso o egreso(clasificar luego)
        if importe >= 0:
            operacion = 60
        else:
            operacion = 61
        # tipo caja 3 coinag
        tipocaja = 3
        registro = {
            'fecha': fecha,
            'monto': abs(float(importe)),
            'observacion': concepto,
            'tipo': tipocaja,
            'operacion': operacion,
            'modified_by': 1,
            'operacionid': id_registro}
        if id_registro not in idoperaciones:
            db['caja'].insert(**registro)
            insertado += 1
        else:
            log(f'duplicado {registro}')
            duplicadas.append(registro)
    db.commit()
    return [f'{insertado} registros insertados',
            duplicadas]


def test_insert_xls_coinag():
    path = 'applications/tapa14/files/upload/2020-12-4/'
    file = '2020-12-4_LaBM_COINAG_2020_10.xls'
    return insert_xls_coinag(path + file)
