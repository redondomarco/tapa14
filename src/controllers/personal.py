
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# for ide
if False:
    import datetime
    from db import db
    from gluon import response, request, auth, cache, redirect, session
    from gluon import CENTER, FORM, DIV, I, A, URL, H4, H5, BR, TAG, INPUT
    from gluon import TABLE, TR, PRE, HTTP
    from gluon import SELECT
    from gluon import SQLFORM
    from gluon.validators import IS_NOT_EMPTY
    from log import log
    from html_helper import grand_button, icon_title
    from personal_empleados import actualizo_marcadas, aplico_politica
    from util import list_dict_to_table_sortable

# ---- example index page ----


def index():
    log('acceso')
    # menu favoritos
    form = CENTER(FORM(
        DIV(I(' Personal', _class='fa fa-ticket fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('empleados',
                             URL('tapa14', 'personal', 'admin_tabla',
                                 vars={'tabla': 'empleado'}),
                             'fa-cart-plus'),
                grand_button('ver marcadas',
                             URL('tapa14', 'personal', 'admin_tabla',
                                 vars={'tabla': 'marcadas'}),
                             'fa-th-large'),
                grand_button('informe mes empleado',
                             URL('tapa14', 'personal', 'informe_mes_empleado'),
                             'fa-truck'),
                grand_button('actualizar marcadas',
                             URL('tapa14', 'personal', 'descarga_marcadas'),
                             'fa-cloud-download'),
                _id='mini_grid'),
            _id='indexdiv'),

        _id='panel_grid'))
    return dict(form=form)


# ---- API (example) -----
# @auth.requires_login()
# def api_get_user_email():
    # if not request.env.request_method == 'GET': raise HTTP(403)
    # return response.json({'status': 'success', 'email': auth.user.email})


# ---- Smart Grid (example) -----
# can only be accessed by members of admin groupd
# @auth.requires_membership('admin')
# def grid():
    # use a generic view
    # response.view = 'generic.html'
    # tablename = request.args(0)
    # if not tablename in db.tables: raise HTTP(403)
    # grid = SQLFORM.smartgrid(db[tablename],
    #                          args=[tablename],
    #                          deletable=False,
    #                          editable=False)
    # return dict(grid=grid)

# ---- Embedded wiki (example) ----
# def wiki():
    # auth.wikimenu() # add the wiki to the menu
    # return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to
    allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def opt_tabla(tabla):
    if tabla == 'cliente':
        fields = ('db.cliente.id, db.cliente.nombre,' +
                  'db.cliente.razon_social,' + 'db.cliente.lista,' +
                  'db.cliente.saldo, db.cliente.tipocuenta, db.cliente.cuit')
    else:
        fields = 'None'
    return {'fields': fields}


def admin_tabla():
    if 'tabla' in request.vars:
        tabla = request.vars['tabla']
        titulo = DIV(
            A(icon_title('fa-arrow-left', 'Volver'), _id='boton_r',
              _class="btn-grid", _href=URL('tapa14', 'personal', 'index')),
            CENTER(H4('Admin ' + (str(tabla).title()))))
        log('acceso grid ' + str(tabla))
        grid = SQLFORM.smartgrid(eval('db.' + str(tabla)),
                                 maxtextlength=20,
                                 linked_tables=['child'],
                                 fields=eval(opt_tabla(tabla)['fields']))
        return dict(grid=grid, titulo=titulo)
    else:
        redirect(URL('index'))


def informe_mes_empleado():
    empleados = db(db.empleado.is_active is True).select(db.empleado.ALL)
    fempl = ([" "] +
             [f"{p.user_code} {p.nombre} {p.apellido}" for p in empleados])
    form = FORM(CENTER(
        H4('Marcadas del personal'),
        TABLE(TR(TAG('<label class "control-label">Persona</label>'),
                 SELECT(fempl, _name='fempleado', _type='text',
                        _id="persona", _class="form-control string")),
              TR(TAG('<label class "control-label">Periodo desde</label>'),
                 INPUT(_name='fdesde', _type='date', _id="mesanio",
                       _class="form-control string",
                       requires=IS_NOT_EMPTY())),
              TR(TAG('<label class "control-label">Periodo hasta</label>'),
                  INPUT(_name='fhasta', _type='date', _id="mesanio",
                        _class="form-control string",))),
        BR(),
        INPUT(_type="submit", _class="btn btn-primary btn-medium",
              _value='Continuar')
    ))
    if form.accepts(request, session):
        session.empleado = request.vars['fempleado']
        session.user_code = request.vars['fempleado'].split()[0]
        session.fdesde = request.vars['fdesde']
        session.fhasta = request.vars['fhasta']
        log(f"seleccionado {session.empleado}")
        log(f"desde: {session.fdesde} hasta {session.fhasta}")
        # selector = (db.empleado.user_code == user_code)
        # usuario = db(selector).select().first().as_dict()
        session.tdesde = datetime.datetime.strptime(session.fdesde, '%Y-%m-%d')
        session.thasta = datetime.datetime.strptime(session.fhasta, '%Y-%m-%d')
        lista = aplico_politica(session.user_code,
                                session.fdesde,
                                session.fhasta)
        nombre_archivo = f'''{session.empleado}
            -{session.fdesde}-{session.fhasta}'''
        session.table = list_dict_to_table_sortable(lista, nombre_archivo)
        session.horas = sumo_horas(lista)
        redirect(URL('informe'))
    else:
        log(f'acceso {request.function}')
    return dict(form=form)


def informe():
    form = CENTER(H5(session.empleado),
                  PRE(f'Desde: {fecha_sp(session.tdesde)} '
                      f'Hasta: {fecha_sp(session.thasta)}'),
                  PRE(f'Total: {session.horas}'),
                  session.table)
    return dict(form=form)


def descarga_marcadas():
    log(f'acceso {request.function}')
    session.mensaje = str(actualizo_marcadas())
    redirect(URL('tapa14', 'default', 'mensajes'))


@auth.requires_login()
def descarga_csv():
    if session.nombre_archivo:
        response.headers['Content-Type'] = 'text/csv'
        attachment = 'attachment;filename='+session.nombre_archivo
        response.headers['Content-Disposition'] = attachment
        # content = session.lista_consulta
        #
        content = open(dir_files + session.nombre_archivo, "r").read()
        log(content)
        raise HTTP(200, str(content),
                   **{'Content-Type': 'text/csv',
                      'Content-Disposition': attachment + ';'})
