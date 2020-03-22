# -*- coding: utf-8 -*-
"""
 funciones sobre el modelo

"""

# for ide
if False:
    from db import db, log
    from util import tree
    import datetime


# no usado aun
# def delete_tables():
#     """borro todo el contenido de las tablas menos los usuarios y permisos"""
#     tables_all = db.tables()
#     try:
#         tables_all.remove('auth_user')
#         tables_all.remove('auth_group')
#         tables_all.remove('auth_permission')
#         tables_all.remove('auth_membership')
#         tables_all.remove('auth_event')
#         tables_all.remove('auth_cas')
#     except Exception:
#         pass
#     for table_name in tables_all:
#         log('borra ' + table_name)
#         try:
#             db[table_name].drop()
#         except Exception as e:
#             log('tabla ' + str(table_name) + ' e: ' + str(e))
#             pass
#     db.commit()


def blank_data():
    tables_all = db.tables()
    # no blanqueo
    try:
        tables_all.remove('auth_user')
        tables_all.remove('auth_group')
        tables_all.remove('auth_permission')
        tables_all.remove('auth_membership')
        tables_all.remove('auth_event')
        tables_all.remove('auth_cas')
    except Exception:
        pass
    for table_name in tables_all:
        try:
            eval('db.' + table_name + '.truncate()')
            log('blanqueo ' + table_name)
        except Exception as e:
            log('error balnqueo ' + str(table_name) + ' e: ' + str(e))
            pass
    db.commit()


def restore_backup(filepath):
    try:
        db.import_from_csv_file(open(filepath, 'r',
                                encoding='utf-8',
                                newline='',),
                                restore=True)
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


def arbol_pedidos():
    pedidos = db(db.pedidos).select(db.pedidos.ALL).as_list()
    fichas = tree()
    for i in pedidos:
        pedidonum = i['pedidonum']
        cantidad = i['cantidad']
        idcliente = i['cliente']
        descuento = i['descuento']
        try:
            fentrega = i['fentrega'].strftime('%d/%m')
        except Exception:
            fentrega = ''
        cliente = db(db.cliente.id == idcliente).select().first()['nombre']
        idproducto = i['producto']
        sel_prod = (db.producto.id == idproducto)
        producto = db(sel_prod).select().first()['nombre_corto']
        nota = i['nota']
        total = i['total']
#        fichas[cliente][pedidonum][producto] = [cantidad,
#                                                nota,
#                                                fentrega,
#                                                total]
        fichas[cliente][pedidonum][producto] = {'cantidad': cantidad,
                                                'nota': nota,
                                                'fentrega': fentrega,
                                                'descuento': descuento,
                                                'total': total}
    return fichas

# devuelve lista de pedidos pendientes


def lista_pedidos():
    pedidos = db(db.pedidos).select(db.pedidos.ALL).as_list()
    lista = []
    for i in pedidos:
        lista.append(int(i['pedidonum']))
    return list(set(lista))


def obtengo_pedido(pedidonum):
    selector = (db.pedidos.pedidonum == pedidonum)
    pedido = db(selector).select(db.pedidos.ALL).as_list()
    if pedido == []:
        return 'error'
    items = []
    for i in pedido:
        selectorp = (db.producto.id == i['producto'])
        producto = db(selectorp).select().first().as_dict()
        detalle = producto['detalle']
        codigo = producto['codigo']
        item = {'cantidad': int(i['cantidad']),
                'producto': detalle,
                'codigo': codigo,
                'descuento': i['descuento'],
                'preciou': i['preciou'],
                'subtotal': i['total']}
        items.append(item)
    resultado = {'cliente_id': pedido[0]['cliente'],
                 'fentrega': pedido[0]['fentrega'],
                 'nota': pedido[0]['nota'],
                 'productos': items}
    return resultado


def elimino_pedido(pedidonum):
    # muevo el pedido a tabla pedidos eliminados
    selector = (db.pedidos.pedidonum == pedidonum)
    pedido = db(selector).select(db.pedidos.ALL).as_list()
    for i in pedido:
        db.pedidos_hist.insert(
            fecha=i['fecha'],
            fentrega=i['fentrega'],
            pedidonum=i['pedidonum'],
            vendedor=i['vendedor'],
            cliente=i['cliente'],
            nota=i['nota'],
            cantidad=i['cantidad'],
            producto=i['producto'],
            preciou=i['preciou'],
            total=i['total']
        )
    db(db.pedidos.pedidonum == pedidonum).delete()
    db.commit()
    log('eliminado pedido:' + str(pedidonum))


def obtengo_cliente(clienteid):
    selector = (db.cliente.id == clienteid)
    return db(selector).select(db.cliente.ALL).as_dict()[clienteid]


# funciones pedido

def listasp():
    '''devuelvo listas de precios'''
    return db(db.listas).select(db.listas.ALL).as_dict()


def ultimo_comprobante(tipo):
    s_cbte = (db.comprobante.nombre == str(tipo))
    comprobante = db(s_cbte).select().first()['lastid']
    return comprobante


def incremento_comprobante(tipo):
    s_ped = (db.comprobante.nombre == tipo)
    db(s_ped).update(lastid=db(s_ped).select()[0].lastid + 1)
    db.commit()


def datos_cliente(cliente):
    s_cliente = (db.cliente.nombre == cliente)
    datos = db(s_cliente).select().first().as_dict()
    # agrego datos de los valores especificos
    s_lista = (db.listas.id == datos['lista'])
    # ordeno lista de productos
    datos['productos'] = sorted(datos['productos'])
    datos['lista_valor'] = db(s_lista).select().first()['valor']
    return datos


def datos_productos():
    datos = db(db.producto).select().as_dict()
    for i in datos:
        s_lista = (db.listas.id == datos[i]['lista'])
        datos[i]['lista_valor'] = db(s_lista).select().first()['valor']
    return datos


def add_stock(cod_id, cantidad):
    log('modifica_stock id: ' + str(cod_id) + ' cant: ' + str(cantidad))
    s_cod = (db.producto.id == cod_id)
    stock = db(s_cod).select().first().as_dict()['stock']
    nuevo = int(stock) + int(cantidad)
    db(s_cod).update(stock=nuevo)
    db.commit()


def add_reserva(cod_id, cantidad):
    log('modifica_reserva cod: ' + str(cod_id) + ' cant: ' + str(cantidad))
    s_cod = (db.producto.id == cod_id)
    stock = db(s_cod).select().first().as_dict()['reserva']
    nuevo = int(stock) + int(cantidad)
    db(s_cod).update(reserva=nuevo)
    db.commit()


def get_producto(codigo):
    selector = (db.producto.codigo == codigo)
    return db(selector).select(db.producto.ALL).first().as_dict()


# hoja de ruta
def agrego_pedido_hdr(pedidonum, hdrnum):
    s_pedido = (db.pedidos.pedidonum == pedidonum)
    idpedido = db(s_pedido).select().first().as_dict()['id']
    log('agrego pedido n ' + str(pedidonum) + ' id: ' + str(idpedido) +
        ' a hoja de ruta n ' + str(hdrnum))
    s_hdr = (db.hoja_de_ruta.numero == hdrnum)
    lista_pedidos = db(s_hdr).select().first()
    if lista_pedidos is None:
        # agrego nueva hoja de ruta
        db.hoja_de_ruta.insert(
            fecha=datetime.datetime.now(),
            numero=hdrnum,
            lista_pedidos=[idpedido])
        db.commit()
    else:
        # hoja de ruta existente
        lista = lista_pedidos.as_dict()['lista_pedidos']
        log(lista)
        if idpedido in lista:
            log('aa')
            pass
        else:
            lista.append(idpedido)
        log(lista)
        db(s_hdr).update(
            lista_pedidos=lista)
        db.commit()


# from sets import Set
# def quito_ce(palabra):
#    caracteres_permitidos='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    allowed_chars = Set(caracteres_permitidos)
#    if palabra==None:
#       return 'error'
#    resultado=''
#    for i in palabra:
#        if i in allowed_chars:
#            resultado=resultado+i
#    return resultado

# if Set(string).issubset(allowed_chars):
#    return string
# else:
#   mensaje='caracter invalido '+str(string)
#    log(mensaje)
#    return ['error',mensaje]
