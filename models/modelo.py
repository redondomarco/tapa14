# -*- coding: utf-8 -*-
"""
Funciones principales de modelo

"""
import datetime

# for ide
if False:
    from gluon import Field, T, request
    from gluon.validators import IS_IN_SET
    from db import auth, db, log
    from util import files_dir
    # from util import *


tipo_producto = ['propio', 'terceros', 'tercerosLM']
tipo_iva = ['RI', 'monotributo', 'consumidor final', 'nc']
tipo_comprobante = ['factura A', 'factura B', 'nota de venta', 'recibo']
tipo_cta = ['contado', 'cta cte']
iva_percent = [21]
estado_pedido = ['pendiente', 'anulado', 'finalizado']
tipo_entrega = ['pendiente', 'entregado']
tipo_pago = ['pendiente', 'parcial', 'pagado', 'cta cte']
tipos_caja = ['B', 'N']
# dir_pdf = ('applications/' + str(configuration.get('datos.app_name')) +
#           '/files/pdf')

db.define_table(
    'listas',
    Field('lista', unique=True, length=255),
    Field('valor', 'double'),
    format='%(lista)s'
)

provincias = {0: 'CIUDAD AUTONOMA BUENOS AIRES',
              1: 'BUENOS AIRES',
              2: 'CATAMARCA',
              3: 'CORDOBA',
              4: 'CORRIENTES',
              5: 'ENTRE RIOS',
              6: 'JUJUY',
              7: 'MENDOZA',
              8: 'LA RIOJA',
              9: 'SALTA',
              10: 'SAN JUAN',
              11: 'SAN LUIS',
              12: 'SANTA FE',
              13: 'SANTIAGO DEL ESTERO',
              14: 'TUCUMAN',
              16: 'CHACO',
              17: 'CHUBUT',
              18: 'FORMOSA',
              19: 'MISIONES',
              20: 'NEUQUEN',
              21: 'LA PAMPA',
              22: 'RIO NEGRO',
              23: 'SANTA CRUZ',
              24: 'TIERRA DEL FUEGO'}


db.define_table(
    'producto',
    Field('codigo', unique=True, length=255),
    Field('nombre_corto', unique=True, length=6),
    Field('detalle', label=T('Nombre del producto'), unique=True, length=255),
    Field('lista', 'reference listas', default=1, notnull=True),
    Field('valor', 'double', default=0, notnull=True),
    Field('stock', 'integer', default=0),
    Field('stock_min', 'integer', default=20),
    Field('stock_max', 'integer', default=500),
    Field('tipo'),
    Field('reserva', 'integer', default=0),
    Field('stock_alias', 'reference producto'),
    auth.signature,
    format='%(detalle)s',
)
db.producto.tipo.requires = IS_IN_SET(tipo_producto)
db.producto._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.producto._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.producto._after_delete.append(
    lambda s: log('delete ' + str(s)))


db.define_table(
    'cliente',
    Field('nombre', unique=True, length=255),
    Field('lista', 'reference listas', notnull=True),
    Field('productos', 'list:reference producto', notnull=True),
    Field('saldo', 'double', default=0),
    Field('tipocuenta', default=tipo_cta[0], notnull=True),
    Field('iva'),
    Field('iva_percent', default=iva_percent[0], notnull=True),
    Field('comprobante', notnull=True),
    Field('correo'),
    Field('aviso', 'boolean'),
    Field('cuit'),
    Field('razon_social'),
    Field('domicilio', length=255),
    Field('localidad', length=255),
    Field('provincia', length=255),
    Field('telefono'),
    auth.signature,
    format='%(nombre)s',
)
db.cliente.iva.requires = IS_IN_SET(tipo_iva)
db.cliente.iva_percent.requires = IS_IN_SET(iva_percent)
db.cliente.comprobante.requires = IS_IN_SET(tipo_comprobante, multiple=True)
db.cliente.tipocuenta.requires = IS_IN_SET(tipo_cta, multiple=True)
db.cliente.provincia.requires = IS_IN_SET(list(provincias.values()))

# tabla de pedidos vigentes
db.define_table(
    'pedidos',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('pedidonum', 'integer', label='N°'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('nota'),
    Field('cantidad', 'integer'),
    Field('descuento', 'integer'),
    Field('producto', 'reference producto', default=1),
    Field('preciou', 'double'),
    Field('total', 'double'),
    auth.signature,
    format='%(pedidonum)s',
)
db.pedidos._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.pedidos._after_delete.append(
    lambda s: log('delete ' + str(s)))

# guardo historico de los pedidos
db.define_table('pedidos_hist',
                db.pedidos,
                Field('estado'))
db.pedidos_hist.estado.requires = IS_IN_SET(estado_pedido)


db.define_table('hoja_de_ruta',
                Field('fecha', 'datetime'),
                Field('numero', 'integer', label='N°'),
                Field('lista_pedidos', 'list:reference pedidos', notnull=True),
                auth.signature)


db.define_table('caja',
                Field('fecha'),
                Field('operacion'),
                Field('tipo'),
                Field('arqueo', 'boolean'),
                auth.signature)
db.caja.tipo.requires = IS_IN_SET(tipos_caja)


db.define_table('bancos',
                Field('nombre'),
                auth.signature)


db.define_table('banco',
                Field('fecha'),
                Field('operacion'),
                Field('tipo'),
                Field('banco', 'reference bancos'),
                Field('arqueo', 'boolean'),
                auth.signature)


db.define_table(
    'ctacte',
    Field('fecha'),
    Field('cliente', 'reference cliente'),
    Field('monto'),
    Field('operacion'),
    Field('comprobante_asoc'),
    auth.signature)



# guardo operaciones
db.define_table(
    'ventas',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('ventanum', 'integer'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('nota'),
    Field('pedido_asoc', 'reference pedidos_hist'),
    Field('total', 'double'),
    Field('comprobante'),
    Field('nro_comprobante', 'integer'),
    Field('entrega'),
    Field('pago'),
    auth.signature,
    format='%(pedidonum)s',
)
db.ventas.comprobante.requires = IS_IN_SET(tipo_comprobante, multiple=True)
db.ventas.entrega.requires = IS_IN_SET(tipo_entrega)
db.ventas.pago.requires = IS_IN_SET(tipo_pago)


# requires = IS_DATE(format=('%d/%m/%Y %H:%M:%S')
db.define_table(
    'ingresos',
    Field('fecha', 'datetime'),
    Field('fecha_prod', 'datetime'),
    Field('ingresonum', 'integer', label='N°'),
    Field('vto', 'datetime'),
    Field('lote', 'integer'),
    Field('usuario', default=auth.user_id),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto'),
    auth.signature
)
db.define_table(
    'es_caja',
    Field('nombre'),
    Field('tipo'),
    auth.signature
)
# db.define_table(
#    'movimientos',
#    Field('fecha', 'datetime'),
#    Field('vendedor', 'reference auth_user'),
#    Field('comprobante', 'integer'),
#    Field('descripcion', 'reference es_caja'),
#    Field('total', 'double')
#    )

db.define_table(
    'comprobante',
    Field('nombre'),
    Field('lastid', 'integer'),
    auth.signature,
)
db.define_table(
    'dinero',
    Field('nombre'),
    Field('valor', 'double'),
    auth.signature,
)
# db.define_table(
#    'pendientes',
#    Field('operacion'),
#    Field('ventanum', 'integer')
#    )

# calcula la fecha de vencimiento para un lote

# materias primas
db.define_table(
    'proveedor',
    Field('nombre'),
    Field('descripcion'),
    auth.signature,
    format='%(nombre)s',
)

db.define_table(
    'tipos_mat_primas',
    Field('nombre'),
    Field('descripcion'),
    auth.signature,
    format='%(nombre)s',
)


db.define_table(
    'marcas',
    Field('nombre'),
    Field('descripcion'),
    auth.signature,
    format='%(nombre)s',
)


db.define_table(
    'mat_primas',
    Field('f_ingreso', 'datetime'),
    Field('cantidad', 'integer'),
    Field('nombre', 'reference tipos_mat_primas'),
    Field('marca', 'reference marcas'),
    Field('proveedor', 'reference proveedor'),
    Field('lote'),
    Field('f_vencimiento', 'datetime'),
    Field('lote_interno'),
    auth.signature)




def fecha_vto(lote):
    diasvto = 30
    a = datetime.datetime.strptime(
        str(datetime.datetime.now().year) + '11', '%Y%m%d')
    b = datetime.timedelta(days=int(lote) + diasvto - 1)
    return a + b


def capture_update():
    log(request.vars.data)
    # return db().insert(data = request.vars.data)


# usurios de sistema
def export_usuarios():
    filepath = files_dir + 'csv-base/db_auth_user.csv'
    rows = db(db.auth_user.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_usuarios():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_auth_user.csv'
    try:
        # borro todo el contenido de la tabla
        db.auth_user.truncate()
        # importo nuevo contenido
        db.auth_user.import_from_csv_file(open(filepath, 'r',
                                          encoding='utf-8',
                                          newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


# grupos de sistema
def export_grupos():
    filepath = files_dir + 'csv-base/db_auth_group.csv'
    rows = db(db.auth_user.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_grupos():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_auth_group.csv'
    try:
        # borro todo el contenido de la tabla
        db.auth_group.truncate()
        # importo nuevo contenido
        db.auth_group.import_from_csv_file(open(filepath, 'r',
                                          encoding='utf-8',
                                          newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]

# pertenencia
def export_grupos():
    filepath = files_dir + 'csv-base/db_auth_membership.csv'
    rows = db(db.auth_user.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_pertenencia():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_auth_membership.csv'
    try:
        # borro todo el contenido de la tabla
        db.auth_membership.truncate()
        # importo nuevo contenido
        db.auth_membership.import_from_csv_file(open(filepath, 'r',
                                          encoding='utf-8',
                                          newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


#productos
def export_grupos():
    filepath = files_dir + 'csv-base/db_productos.csv'
    rows = db(db.productos.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))

def populate_producto():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_producto.csv'
    try:
        # borro todo el contenido de la tabla
        db.producto.truncate('RESTART IDENTITY CASCADE')
        # importo nuevo contenido
        db.producto.import_from_csv_file(open(filepath, 'r',
                                          encoding='utf-8',
                                          newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


# productos
def export_listas():
    filepath = files_dir + 'csv-base/db_listas.csv'
    rows = db(db.listas.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_listas():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_listas.csv'
    try:
        # borro todo el contenido de la tabla
        db.listas.truncate()
        # importo nuevo contenido
        db.listas.import_from_csv_file(open(filepath, 'r',
                                       encoding='utf-8',
                                       newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


def export_cliente():
    filepath = files_dir + 'csv-base/db_cliente.csv'
    rows = db(db.cliente.id).select()
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_cliente():
    # leo de files csv
    filepath = files_dir + 'csv-base/db_cliente.csv'
    try:
        # borro todo el contenido de la tabla
        db.cliente.truncate('RESTART IDENTITY CASCADE')
        # importo nuevo contenido
        db.cliente.import_from_csv_file(open(filepath, 'r',
                                        encoding='utf-8',
                                        newline='',))
        db.commit()
        mensaje = 'cargado sin errores'
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


def export_table(db_name, table_name):
    filename = str(db_name) + '_' + str(table_name) + '.csv'
    filepath = files_dir + 'csv-base/' + filename
    rows = eval(db_name + '(' + db_name + '.' + table_name + '.id).select()')
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_table(db_name, table_name):
    # leo de files csv
    filepath = files_dir + 'csv-base/db_' + str(table_name) + '.csv'
    # filename = str(db_name) + '_' + str(table_name) + '.csv'
    try:
        # borro todo el contenido de la tabla
        #eval(db_name + '.' + table_name + """.truncate('RESTART IDENTITY CASCADE')""")
        # importo nuevo contenido
        eval(db_name + '.' + table_name +
             """.import_from_csv_file(open(filepath, 'r', encoding='utf-8', newline=''))""")
        eval(db_name + '.commit()')
        mensaje = str(table_name) + ' cargado sin errores en ' + str(db_name)
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


def truncate_all_db(db_name, table_name):
    eval(db_name + '.' + table_name + """.truncate('RESTART IDENTITY CASCADE')""")
    
# para regenerar tablas se puede borrar todo el contenido de la carpeta
# databases:
# rm databases/*


# es importante el orden
tablas = ['auth_user', 'auth_group', 'auth_membership',
          'listas', 'cliente',
          'producto', 'comprobante',
          'proveedor', 'marcas', 'tipos_mat_primas',
          'mat_primas']

base = 'db'


def export_all_csv():
    for tabla in tablas:
        export_table(base, tabla)


def populate_accesos_base():
    # blanqueo toda la base
    for tabla in tablas:
        truncate_all_db(base, tabla)
    # completo con los datos del export
    for tabla in tablas:
        ejecuta = populate_table(base, tabla)
        log(ejecuta)
