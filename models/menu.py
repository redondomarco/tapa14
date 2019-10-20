# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

response.menu = []

# menucalculadora = (T('test'), False, URL('default', 'index2'), [])
menutest = (T('lista de funciones'), False, None,
            [(T('calculadora'), False,
             URL(request.application, 'default', 'index2')),
            (T('venta'), False,
             URL(request.application, 'default', 'venta')),
            (T('ingreso'), False,
             URL(request.application, 'default', 'ingreso')),
            (T('ventaold'), False,
             URL(request.application, 'default', 'ventaold')),
             ]
            )
menuvendedor = (T('Venta'), False, URL('default', 'venta'), [])
menureserva = (T('Reserva'), False, URL('default', 'reserva'), [])
menuingreso = (T('Ingreso'), False, URL('default', 'ingreso'), [])


menupedido = ('Pedidos', False, '#',
              [(T('Nuevo'), False,
               URL('default', 'selec_cliente_pedido')),
              (T('Listado'), False,
               URL('default', 'pedido_pendiente'))
               ]
              )

menufacturas = (T('Comprobantes'), False, None,
                [(T('Subir facturas'), False,
                 URL('default', 'subir_facturas')),
                (T('Procesar facturas'), False,
                 URL('default', 'procesar_facturas')),
                (T('subir datos afip'), False,
                 URL('default', 'subir_datos_afip_paso1')),
                (T('Lista'), False, URL('default', 'lista_fa')),
                (T('Despacho'), False, URL('default', 'lista_despacho'))
                 ]
                )
menuappadmin = (T('appadmin'), False, URL('appadmin', 'index'), [])

menuconf = (I(' Config', _class='fa fa-gear'), False, URL('default', 'admin'))

menuadmin = (T('General'), False, '#',
             [(T('Archivo'), False, URL('default', 'archivo')),
              (T('Guardar Backup'), False, URL('default', 'save_backup')),
              (T('Restaurar Backup'), False, URL('default', 'load_backup')),
              (T('admin'), False, URL('default', 'admin')),
              ]
             )

# response.menu.append(menucalculadora)

if auth.user:
    selector1 = (db.auth_membership.user_id == auth.user.id)
    selector2 = (db.auth_membership.group_id == db.auth_group.id)
    groups = db(selector1 & selector2).select(db.auth_group.role)
# logger.info(str(groups))
# logger.info(str(auth.user))
    for group in groups:
        if group.role == 'vendedor':
            pass
            #response.menu.append(menupedido)
# response.menu.append(menureserva)
# if group.role == 'productor':
#  response.menu.append(menuingreso)
# if group.role == 'cliente':
#   response.menu.append(menucliente)
        if group.role == 'admin':
            response.menu.append(menuadmin)
            response.menu.append(menufacturas)
            response.menu.append(menuconf)
        if auth.user.email == 'redondomarco@gmail.com':
            #response.menu.append(menuappadmin)
            pass
# response.menu.append(menucalculadora)
# response.menu.append(menutest)


# ----------------------------------------------------------------------------
# provide shortcuts for development. you can
# remove everything below in production
# ----------------------------------------------------------------------------

# if not configuration.get('app.production'):
#     _app = request.application
#     response.menu += [
#         (T('My Sites'), False, URL('admin', 'default', 'site')),
#         (T('This App'), False, '#', [
#             (T('Design'), False, URL('admin', 'default',
#                                      'design/%s' % _app)),
#             (T('Controller'), False,
#              URL(
#                  'admin', 'default', 'edit/%s/controllers/%s.py' % (
#                       _app, request.controller))),
#             (T('View'), False,
#              URL(
#                  'admin', 'default', 'edit/%s/views/%s' % (
#                       _app, response.view))),
#             (T('DB Model'), False,
#              URL(
#                  'admin', 'default', 'edit/%s/models/db.py' % _app)),
#             (T('Menu Model'), False,
#              URL(
#                  'admin', 'default', 'edit/%s/models/menu.py' % _app)),
#             (T('Config.ini'), False,
#              URL(
#                  'admin', 'default',
#                  'edit/%s/private/appconfig.ini' % _app)),
#             (T('Layout'), False,
#              URL(
#                  'admin', 'default', 'edit/%s/views/layout.html' % _app)),
#             (T('Stylesheet'), False,
#              URL(
#                  'admin', 'default',
#                  'edit/%s/static/css/web2py-bootstrap3.css' % _app)),
#             (T('Database'), False, URL(_app, 'appadmin', 'index')),
#             (T('Errors'), False, URL(
#                 'admin', 'default', 'errors/' + _app)),
#             (T('About'), False, URL(
#                 'admin', 'default', 'about/' + _app)),
#         ]),
#         ('web2py.com', False, '#', [
#             (T('Download'), False,
#              'http://www.web2py.com/examples/default/download'),
#             (T('Support'), False,
#              'http://www.web2py.com/examples/default/support'),
#             (T('Demo'), False, 'http://web2py.com/demo_admin'),
#             (T('Quick Examples'), False,
#              'http://web2py.com/examples/default/examples'),
#             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
#             (T('Videos'), False,
#              'http://www.web2py.com/examples/default/videos/'),
#             (T('Free Applications'),
#              False, 'http://web2py.com/appliances'),
#             (T('Plugins'), False, 'http://web2py.com/plugins'),
#             (T('Recipes'), False, 'http://web2pyslices.com/'),
#         ]),
#         (T('Documentation'), False, '#', [
#             (T('Online book'), False, 'http://www.web2py.com/book'),
#             (T('Preface'), False,
#              'http://www.web2py.com/book/default/chapter/00'),
#             (T('Introduction'), False,
#              'http://www.web2py.com/book/default/chapter/01'),
#             (T('Python'), False,
#              'http://www.web2py.com/book/default/chapter/02'),
#             (T('Overview'), False,
#              'http://www.web2py.com/book/default/chapter/03'),
#             (T('The Core'), False,
#              'http://www.web2py.com/book/default/chapter/04'),
#             (T('The Views'), False,
#              'http://www.web2py.com/book/default/chapter/05'),
#             (T('Database'), False,
#              'http://www.web2py.com/book/default/chapter/06'),
#             (T('Forms and Validators'), False,
#              'http://www.web2py.com/book/default/chapter/07'),
#             (T('Email and SMS'), False,
#              'http://www.web2py.com/book/default/chapter/08'),
#             (T('Access Control'), False,
#              'http://www.web2py.com/book/default/chapter/09'),
#             (T('Services'), False,
#              'http://www.web2py.com/book/default/chapter/10'),
#             (T('Ajax Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/11'),
#             (T('Components and Plugins'), False,
#              'http://www.web2py.com/book/default/chapter/12'),
#             (T('Deployment Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/13'),
#             (T('Other Recipes'), False,
#              'http://www.web2py.com/book/default/chapter/14'),
#             (T('Helping web2py'), False,
#              'http://www.web2py.com/book/default/chapter/15'),
#             (T("Buy web2py's book"), False,
#              'http://stores.lulu.com/web2py'),
#         ]),
#         (T('Community'), False, None, [
#             (T('Groups'), False,
#              'http://www.web2py.com/examples/default/usergroups'),
#             (T('Twitter'), False, 'http://twitter.com/web2py'),
#             (T('Live Chat'), False,
#              'http://webchat.freenode.net/?channels=web2py'),
#         ]),
#     ]

