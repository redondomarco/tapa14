# db.define_table(
#   'imagen',
#   Field('titulo', unique=True, length=255),
#   Field('archivo', 'upload'),
#   format = '%(titulo)s')

# combos cliente

# for ide
if False:
    from db import *
    from util import *


tipo_iva = ['RI', 'monotributo', 'consumidor final', 'nc']
tipo_comprobante = ['factura A', 'factura B', 'nota de venta', 'recibo']
tipo_cta = ['contado', 'cta cte']
estado_pedido = ['borrado', 'vendido']
dir_pdf = ('applications/' + str(configuration.get('datos.app_name')) +
           '/files/pdf')

db.define_table(
    'producto',
    Field('codigo', unique=True, length=255),
    Field('detalle', label=T('Nombre del producto'), unique=True, length=255),
    Field('valor', 'double', default=0),
    Field('stock', 'integer', default=0),
    Field('reserva', 'integer', default=0),
    Field('stock_alias', 'reference producto'),
    format='%(detalle)s'
)
db.define_table(
    'listas',
    Field('lista', unique=True, length=255),
    Field('valor', 'double'),
    format='%(lista)s'
)

db.define_table(
    'cliente',
    Field('nombre', unique=True, length=255),
    Field('lista', 'reference listas'),
    Field('productos', 'list:reference producto'),
    Field('saldo', 'double', default=0),
    Field('tipocuenta', default=tipo_cta[0]),
    Field('iva'),
    Field('comprobante'),
    Field('correo'),
    Field('aviso', 'boolean'),
    Field('cuit'),
    Field('razon_social'),
    Field('domicilio', length=255),
    Field('localidad', length=255),
    Field('provincia', length=255),
    Field('telefono'),
    Field('activo', 'boolean'),
    format='%(nombre)s'
)
db.cliente.iva.requires = IS_IN_SET(tipo_iva)
db.cliente.comprobante.requires = IS_IN_SET(tipo_comprobante, multiple=True)
db.cliente.tipocuenta.requires = IS_IN_SET(tipo_cta, multiple=True)

# tabla de pedidos
db.define_table(
    'pedidos',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('pedidonum', 'integer'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('nota'),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto', default=1),
    Field('preciou', 'double'),
    Field('total', 'double'),
    format='%(pedidonum)s'
)

db.define_table(
    'pedidos_hist',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('pedidonum', 'integer'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('nota'),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto', default=1),
    Field('preciou', 'double'),
    Field('total', 'double'),
    format='%(pedidonum)s'
)

# ventas
#  estados
tipo_entrega = ['pendiente', 'entregado']
tipo_pago = ['pendiente', 'parcial', 'pagado']
estado_pedido = ['pendiente', 'anulado', 'finalizado']
#  tabla de ventas
db.define_table(
    'ventas',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('ventanum', 'integer'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('nota'),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto', default=1),
    Field('preciou', 'double'),
    Field('total', 'double'),
    Field('comprobante'),
    Field('nro_comprobante', 'integer'),
    Field('entrega'),
    Field('pago'),
    format='%(pedidonum)s'
)
db.ventas.comprobante.requires = IS_IN_SET(tipo_comprobante, multiple=True)
db.ventas.entrega.requires = IS_IN_SET(tipo_entrega)
db.ventas.pago.requires = IS_IN_SET(tipo_pago)


# requires = IS_DATE(format=('%d/%m/%Y %H:%M:%S')
db.define_table(
    'ingresos',
    Field('fecha', 'datetime'),
    Field('fecha_prod', 'datetime'),
    Field('vto', 'datetime'),
    Field('lote', 'integer'),
    Field('usuario', default=auth.user_id),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto')
)
db.define_table(
    'es_caja',
    Field('nombre'),
    Field('tipo')
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
    Field('lastid', 'integer')
)
db.define_table(
    'dinero',
    Field('nombre'),
    Field('valor', 'double')
)
# db.define_table(
#    'pendientes',
#    Field('operacion'),
#    Field('ventanum', 'integer')
#    )

# calcula la fecha de vencimiento para un lote


def fecha_vto(lote):
    diasvto = 30
    a = datetime.strptime(str(datetime.now().year) + '11', '%Y%m%d')
    b = timedelta(days=int(lote) + diasvto - 1)
    return a + b


def capture_update():
    log(request.vars.data)
    # return db().insert(data = request.vars.data)