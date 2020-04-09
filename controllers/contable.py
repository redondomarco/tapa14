# -*- coding: utf-8 -*-

# for ide
if False:
    from gluon import auth
    from gluon import request, session
    from gluon import SQLFORM
    from gluon import URL, redirect
    from gluon import DIV, FORM, CENTER, TABLE, TR, H4, TAG, BR, INPUT, PRE
    from gluon import SELECT
    from gluon.validators import IS_NOT_EMPTY
    from db import db
    from html_helper import opt_tabla
    from log import log
    from cajas import movimientos_cajas, proceso_mov_cajas, get_cajas
    from util import list_dict_to_table_sortable


@auth.requires_membership('oficina_data_entry')
def consulta_caja():
    log('acceso ' + str(request.function))
    grid = SQLFORM.grid(
        db.caja,
        fields=(db.caja.fecha,
                db.caja.operacion,
                db.caja.persona,
                db.caja.tipo,
                db.caja.comprobante,
                db.caja.nro_cbte,
                db.caja.monto,
                db.caja.observacion
                ),
        searchable=True,
        editable=False,
        deletable=False,
        create=True,
        sortable=True,
        details=True,
        maxtextlength=25)
    return dict(grid=grid)


@auth.requires_login()
def entry_tabla():
    if 'tabla' in request.vars:
        tabla = request.vars['tabla']
        titulo = DIV(
            CENTER(H4('Admin ' + (str(tabla).title()))))
        log('acceso grid ' + str(tabla))
        grid = SQLFORM.grid(eval('db.' + str(tabla)),
                            maxtextlength=20,
                            deletable=False,
                            fields=eval(opt_tabla(tabla)['fields']))
        return dict(grid=grid, titulo=titulo)
    else:
        redirect(URL('index'))


def mov_caja_sel_fecha():
    cajas = get_cajas()
    form = FORM(CENTER(
        H4('Movimientos de Caja'),
        TABLE(TR(TAG('<label class "control-label">Tipo</label>'),
                 SELECT(cajas, _name='fcaja', _type='text',
                        _id="ftcaja", _class="form-control string")),
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
        tipo = request.vars['fcaja']
        fdesde = request.vars['fdesde']
        fhasta = request.vars['fhasta']
        log(f"reporte caja : {tipo} desde: {fdesde} hasta {fhasta}")
        movimientos = movimientos_cajas(fdesde, fhasta, tipo)
        proceso = proceso_mov_cajas(movimientos)
        tabla = proceso[0]
        ingresos = proceso[1]
        egresos = proceso[2]
        n_archivo = 'mov_caja_'
        orden = ['fecha', 'persona', 'cuenta', 'caja', 'cbte', 'nro_cbte',
                 'egreso', 'ingreso', 'operador', 'obs']
        divmensaje = list_dict_to_table_sortable(tabla, n_archivo, orden)
        session.mensaje = DIV(
            CENTER(divmensaje),
            PRE(f'Total Ingresos: {round(ingresos,2)}'),
            PRE(f'Total Egresos: {round(egresos,2)}'),
            PRE(f'Resultado: {round((ingresos-egresos),2)}'),
            _style='width:100%;overflow-x:auto;-ms-overflow-x:scroll',
        )
        redirect(URL('tapa14', 'default', 'mensajes'))
        # selector = (db.empleado.user_code == user_code)
        # usuario = db(selector).select().first().as_dict()
        # redirect(URL('informe'))
    else:
        log(f'acceso {request.function}')
    return dict(form=form)
