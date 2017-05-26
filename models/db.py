# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

#db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'], migrate=True)
db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'], lazy_tables=True)
#db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'],lazy_tables=True)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager
from gluon.serializers import json


auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

#import-varios
import datetime
from datetime import datetime,date,timedelta

#logger
import logging
logger = logging.getLogger("web2py")
logger.setLevel(logging.DEBUG)
log_remove = [
'Set-Cookie: ',
'session_id_tapa14=']

def log(palabra):
    """funcion auxiliar de auditoria que incorpora el usuario si es que existe"""
    if hasattr(auth.user, 'email'):
        mensaje=str(auth.user.email)+' '+str(request.cookies)+' '+str(request.function)+' '+str(palabra)
        for i in log_remove:
            mensaje = mensaje.replace(str(i),'')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin '+str(palabra))

def debug(palabra):
    if hasattr(auth.user, 'email'):
        mensaje='DEBUG-'+str(palabra)+'-FIN'
        for i in log_remove:
            mensaje = mensaje.replace(str(i),'')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin '+str(palabra))
## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

#db.define_table(
#   'imagen',
#   Field('titulo', unique=True, length=255),
#   Field('archivo', 'upload'),
#   format = '%(titulo)s')

db.define_table(
    'producto',
    Field('codigo', unique=True, length=255),
    Field('detalle', label=T('Nombre del producto'), unique=True, length=255),
    Field('valor', 'double'),
    Field('stock', 'integer'),
    Field('reserva', 'integer'),
    Field('stock_alias', 'reference producto'),
    format='%(detalle)s'
    )
db.define_table(
    'listas',
    Field('lista', unique=True, length=255),
    Field('valor', 'double'),
    format='%(lista)s'
    )
db.define_table('tipo_cta',
                Field('tipo', label=('Tipos de cuenta')),
                format='%(tipo)s')
db.define_table(
    'cliente',
    Field('nombre', unique=True, length=255),
    Field('lista', 'reference listas'),
    Field('productos', 'list:reference producto'),
    Field('saldo', 'double', default=0),
    Field('tipocuenta','reference tipo_cta'),
    format='%(nombre)s'
    )
db.define_table(
    'ventas',
    Field('fecha', 'datetime'),
    Field('fentrega', 'datetime'),
    Field('ventanum', 'integer'),
    Field('vendedor', 'reference auth_user'),
    Field('cliente', 'reference cliente'),
    Field('cantidad', 'integer'),
    Field('producto', 'reference producto'),
    Field('preciou', 'double'),
    Field('total', 'double'),
    format='%(ventanum)s'
    )
#requires = IS_DATE(format=('%d/%m/%Y %H:%M:%S')
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
db.define_table(
    'movimientos',
    Field('fecha', 'datetime'),
    Field('vendedor', 'reference auth_user'),
    Field('comprobante', 'integer'),
    Field('descripcion', 'reference es_caja'),
    Field('total', 'double')
    )
db.define_table(
    'comprobante',
    Field('nombre'),
    Field('lastid', 'integer')
    )
db.define_table(
    'dinero',
    Field('nombre'),
    Field('valor','double')
    )
db.define_table(
    'pendientes',
    Field('operacion'),
    Field('ventanum', 'integer')
    )
def fecha_vto(lote):
    diasvto=30
    a=datetime.strptime(str(datetime.now().year)+'11','%Y%m%d')
    b=timedelta(days=int(lote)+diasvto-1)
    return a+b