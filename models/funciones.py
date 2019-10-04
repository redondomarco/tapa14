# funciones sobre el modelo

# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

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
        try:
            fentrega = i['fentrega'].strftime('%d/%m')
        except Exception:
            fentrega = ''
        cliente = db(db.cliente.id == idcliente).select().first()['nombre']
        idproducto = i['producto']
        producto = db(db.producto.id == idproducto).select().first()['nombre_corto']
        nota = i['nota']
        total = i['total']
        fichas[cliente][pedidonum][producto] = [cantidad,
                                                nota,
                                                fentrega,
                                                total]
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
    cliente_id = pedido[0]['cliente']
    fentrega = pedido[0]['fentrega']
    nota = pedido[0]['nota']
    items = []
    for i in pedido:
        selectorp = (db.producto.id == i['producto'])
        producto = db(selectorp).select().first()['codigo']
        item = [(int(i['cantidad']), producto, i['preciou'])]
        items.append(item)
    return [cliente_id, fentrega, nota, items]


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
