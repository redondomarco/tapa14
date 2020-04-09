# -*- coding: utf-8 -*-

if False:
    from db import db
    from log import log
    from util import str_to_date


def get_cajas():
    cajas = db(db.tipos_caja).select().as_dict()
    resultado = []
    for i in cajas:
        if cajas[i]['is_active']:
            resultado.append(cajas[i]['nombre'])
    return resultado


def arqueo_caja(fecha):
    pass


def movimientos_cajas(fdesde, fhasta, tipo):
    """devuelvo movimientos de un tipo de caja entre fechas"""
    tipoid = db(db.tipos_caja.nombre == tipo).select().first()['id']
    moves = db((db.caja.fecha >= str_to_date(fdesde)) &
               (db.caja.fecha <= str_to_date(fhasta)) &
               (db.caja.tipo == tipoid)).select()
    return moves.as_dict()


def test_movimientos_cajas():
    fdesde = '2020-04-01'
    fhasta = '2020-04-01'
    tipo = 'Linea 2'
    return movimientos_cajas(fdesde, fhasta, tipo)


def proceso_mov_cajas(moves):
    ctop = tipos_op()
    cpers = personas()
    tcbte = tipos_cbtes()
    movimientos = []
    autores = usuarios_sistema()
    ccaja = tipos_caja()
    sum_ingresos = float(0)
    sum_egresos = 0
    for registro in moves:
        # segun tipo operacion
        log(registro)
        operacionid = moves[registro]['operacion']
        tipo_op = ctop[operacionid]['tipo']
        if tipo_op == 'ingreso':
            ingreso = moves[registro]['monto']
            egreso = ''
            sum_ingresos += float(moves[registro]['monto'])
        elif tipo_op == 'egreso':
            ingreso = ''
            egreso = moves[registro]['monto']
            sum_egresos += float(moves[registro]['monto'])
        else:
            log('definir nueva operacion!')
            ingreso = ''
            egreso = ''
        try:
            cbte = tcbte[moves[registro]['comprobante']]['nombre']
        except Exception:
            cbte = ''
        try:
            persona = cpers[moves[registro]['persona']]['nombre']
        except Exception:
            persona = ''
        movimientos.append({
            'fecha': moves[registro]['fecha'],
            'nro_cbte': moves[registro]['nro_cbte'],
            'cuenta': ctop[operacionid]['nombre'],
            'egreso': egreso,
            'ingreso': ingreso,
            'operador': autores[moves[registro]['modified_by']]['first_name'],
            'caja': ccaja[moves[registro]['tipo']]['nombre'],
            'cbte': cbte,
            'persona': persona,
            'obs': moves[registro]['observacion']
        })
    return [movimientos, sum_ingresos, sum_egresos]


def test_proceso_mov_cajas():
    return proceso_mov_cajas(test_movimientos_cajas())


def tipos_op():
    return db(db.tipos_cuenta.is_active).select().as_dict()


def personas():
    return db(db.personas).select().as_dict()


def tipos_cbtes():
    return db(db.tipos_comprobante).select().as_dict()


def usuarios_sistema():
    return db(db.auth_user).select().as_dict()


def tipos_caja():
    return db(db.tipos_caja).select().as_dict()
