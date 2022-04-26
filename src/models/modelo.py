# -*- coding: utf-8 -*-
"""
Funciones principales de modelo

"""
import datetime
from collections import OrderedDict

# for ide
if 1 == 2:
    from gluon import Field, T, request
    from gluon.validators import IS_IN_SET
    from db import auth, db
    from log import log
    from util import files_dir, csv_to_list_of_dict
    from util import os, csv, idtemp_generator
    # from util import *


tipo_producto = ['propio', 'terceros', 'tercerosLM', 'tercerosVD']
tipo_iva = ['RI', 'monotributo', 'consumidor final', 'nc']
tipo_cta = ['contado', 'cta cte']
iva_percent = [21]
estado_pedido = ['pendiente', 'anulado', 'finalizado']
tipo_entrega = ['pendiente', 'entregado']
tipo_pago = ['pendiente', 'parcial', 'pagado', 'cta cte']

# dir_pdf = ('applications/' + str(configuration.get('datos.app_name')) +
# '/files/pdf')

db.define_table(
    'listas',
    Field('lista', unique=True, length=255),
    Field('valor', 'double'),
    auth.signature,
    format='%(lista)s'
)
db.listas._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.listas._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.listas._after_delete.append(
    lambda s: log('delete ' + str(s)))

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
    'localidad',
    Field('codigo', unique=True, length=255),
    Field('nombre', unique=True, length=30),
    auth.signature,
    format='%(nombre)s',
)

db.define_table(
    'tipos_caja',
    Field('codigo', unique=True, length=255),
    Field('nombre', unique=True, length=30),
    auth.signature,
    format='%(nombre)s',
)
db.tipos_caja._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.tipos_caja._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.tipos_caja._after_delete.append(
    lambda s: log('delete ' + str(s)))

db.define_table(
    'tipos_comprobante',
    Field('codigo', unique=True, length=255),
    Field('nombre', unique=True, length=30),
    auth.signature,
    format='%(nombre)s',
)
db.tipos_comprobante._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.tipos_comprobante._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.tipos_comprobante._after_delete.append(
    lambda s: log('delete ' + str(s)))

db.define_table(
    'tipos_cod_cuenta',
    Field('codigo', unique=True, length=30),
    auth.signature,
    format='%(codigo)s',
)

db.define_table(
    'tipos_cuenta',
    Field('nombre', unique=True, length=30),
    Field('codigo', length=30),
    Field('tipo'),
    auth.signature,
    format='%(nombre)s',
)
db.tipos_cuenta.tipo.requires = IS_IN_SET(['ingreso', 'egreso'])
db.tipos_cuenta._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.tipos_cuenta._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.tipos_cuenta._after_delete.append(
    lambda s: log('delete ' + str(s)))


db.define_table(
    'personas',
    Field('nombre', unique=True, length=255),
    Field('correo'),
    Field('cuit'),
    Field('comprobante', 'list:reference tipos_comprobante'),
    Field('razon_social'),
    Field('domicilio', length=255),
    Field('dia_horario', length=600),
    Field('nota', length=1000),
    Field('geomap', length=600),
    Field('link', length=400),
    Field('provincia', length=255),
    Field('localidad', 'reference localidad', default=1),
    Field('telefono'),
    auth.signature,
    format='%(nombre)s'
)
db.personas.provincia.requires = IS_IN_SET(list(provincias.values()))
db.personas._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.personas._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.personas._after_delete.append(
    lambda s: log('delete ' + str(s)))


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
    Field('aviso', 'boolean'),
    Field('persona', 'reference personas'),
    # Field('correo'),
    # Field('cuit'),
    # Field('comprobante', notnull=True),
    # Field('razon_social'),
    # Field('domicilio', length=255),
    # Field('localidad', length=255),
    # Field('provincia', length=255),
    # Field('telefono'),
    auth.signature,
    format='%(nombre)s',
)
db.cliente.iva.requires = IS_IN_SET(tipo_iva)
db.cliente.iva_percent.requires = IS_IN_SET(iva_percent)
db.cliente.tipocuenta.requires = IS_IN_SET(tipo_cta, multiple=True)

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
                Field('fecha', 'date'),
                Field('operacion', 'reference tipos_cuenta'),
                Field('tipo', 'reference tipos_caja'),
                Field('persona', 'reference personas'),
                Field('comprobante', 'reference tipos_comprobante'),
                Field('nro_cbte'),
                Field('observacion'),
                Field('operacionid'),
                Field('monto', 'double', notnull=True),
                auth.signature)
db.caja._after_insert.append(
    lambda f, i: log('insert ' + str(f) + ' ' + str(i)))
db.caja._after_update.append(
    lambda s, f: log('update ' + str(s) + ' ' + str(f)))
db.caja._after_delete.append(
    lambda s: log('delete ' + str(s)))


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
    Field('comprobante', 'reference tipos_comprobante'),
    Field('nro_comprobante', 'integer'),
    Field('entrega'),
    Field('pago'),
    auth.signature,
    format='%(pedidonum)s',
)
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
    Field('persona', 'reference personas'),
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


# productos
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


def export_table(db_name, table_name, **kwargs):
    filename = str(db_name) + '_' + str(table_name) + '.csv'
    hoy = datetime.datetime.today()
    if 'backup' in kwargs:
        try:
            dirfecha = str(hoy.year) + str(hoy.month) + str(hoy.day)
            directorio = files_dir + 'backup/' + dirfecha
            os.makedirs(directorio)
        except Exception:
            pass
        filepath = files_dir + 'backup/' + dirfecha + '/' + filename
    else:
        filepath = files_dir + 'csv-base/' + filename
    rows = eval(db_name + '(' + db_name + '.' + table_name + '.id).select()')
    rows.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))


def populate_table(db_name, table_name):
    # leo de files csv
    filepath = files_dir + 'csv-base/db_' + str(table_name) + '.csv'
    log(f'cargo {filepath}')
    filepath = prepare_csv(filepath)
    # filename = str(db_name) + '_' + str(table_name) + '.csv'
    try:
        # importo nuevo contenido
        eval(db_name + '.' + table_name +
             """.import_from_csv_file(open(filepath, 'r',
             encoding='utf-8', newline=''),)""")
        eval(db_name + '.commit()')
        mensaje = str(table_name) + ' cargado sin errores en ' + str(db_name)
        log(mensaje)
        return ['ok', mensaje]
    except Exception as e:
        return ['error', str(e)]


def truncate_all_db(db_name, table_name):
    """borro todo el contenido de la tabla"""
    eval(db_name + '.' + table_name +
         """.truncate('RESTART IDENTITY CASCADE')""")
    eval(db_name + '.commit()')

# para regenerar tablas se puede borrar todo el contenido de la carpeta
# databases:
# rm databases/*


# es importante el orden
tablas = ['auth_user', 'auth_group', 'marcadas',
          'auth_membership', 'auth_event', 'localidad',
          'listas', 'tipos_cod_cuenta', 'comprobante',
          'tipos_comprobante', 'tipos_caja',
          'tipos_mat_primas', 'empleado', 'marcas', 'bancos',
          'tipos_cuenta', 'personas', 'banco',
          'producto', 'proveedor', 'caja',
          'cliente', 'ingresos', 'mat_primas',
          'pedidos', 'pedidos_hist', 'ctacte',
          'hoja_de_ruta', 'ventas']

base = 'db'


def export_all_csv(**kwargs):
    """ Exporta todas las tablas al directorio csv-base
    export_all_csv()

    Opcional:
    export_all_csv(backup=True)
    para guardar el backup actual directorio backup/$fecha """
    if 'backup' in kwargs:
        for tabla in tablas:
            export_table(base, tabla, backup=True)
    else:
        for tabla in tablas:
            export_table(base, tabla)
    return 'recordar pushear data en files de github'


def truncate_all():
    # blanqueo toda la base
    for tabla in tablas:
        truncate_all_db(base, tabla)


def populate_accesos_base():
    # blanqueo toda la base
    for tabla in tablas:
        truncate_all_db(base, tabla)
    # completo con los datos del export
    for tabla in tablas:
        # ejecuta = populate_table(base, tabla)
        # log(ejecuta)
        restore(tabla)
    # reparo id autoincrement
    filepath = export_all()
    import_all(filepath)


def prepare_csv(filepath):
    filepath_out = filepath + 'r'
    resultado = {}
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        claves = reader.fieldnames
        for row in reader:
            resultado[int(row[claves[0]])] = row
    # return resultado
    # return claves
    maxid = max(resultado.keys())
    tocsv = {}
    for i in range(1, maxid):
        try:
            tocsv[i] = resultado[i]
        except Exception:
            reg_vacio = []
            for j in claves:
                if '.id' in j:
                    reg_vacio.append((j, i))
                else:
                    reg_vacio.append((j, ''))
            tocsv[i] = OrderedDict(reg_vacio)
    # return tocsv
    with open(filepath_out, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=claves)
        writer.writeheader()
        for i in tocsv:
            writer.writerow(tocsv[i])
    log(f'procesado {filepath_out}')
    return filepath_out


def test_prepare_csv():
    filepath = files_dir + 'csv-base/db_tipos_cuenta.csv'
    return prepare_csv(filepath)


def restore(tabla):
    # truncate_all_db(base, tabla)
    filepath = files_dir + 'csv-base/db_' + str(tabla) + '.csv'
    log(f'restore {filepath}')
    filas = csv_to_list_of_dict(filepath)[1]
    for fila in filas:
        filaproc = {}
        for i in fila:
            clave = i.split('.')[1]
            valor = fila[i]
            if valor == '<NULL>':
                valor = ''
            # migracion mediante borrar
            elif tabla == 'tipos_cuenta' and clave == 'codigo':
                valor = ''
            elif tabla == 'personas' and clave == 'comprobante':
                valor = ''
            elif tabla == 'cliente' and clave == 'productos':
                valor = valor.split('|')
            elif tabla == 'hoja_de_ruta' and clave == 'lista_pedidos':
                valor = valor.split('|')                
            filaproc[clave] = valor
        log(f'{base}.{tabla}.insert(**{filaproc})')
        eval(f'{base}.{tabla}.insert(**{filaproc})')
    db.commit()


def export_all():
    filepath = f'{files_dir}csv-base/todo_{idtemp_generator(4)}.csv'
    db.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))
    log(f'generado {filepath}')
    return filepath


def import_all(filepath):
    truncate_all()
    db.import_from_csv_file(open(filepath, 'r', encoding='utf-8', newline=''))
    db.commit()
