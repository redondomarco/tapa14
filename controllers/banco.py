# -*- coding: utf-8 -*-

import pandas as pd
import json2html
# for ide
if False:
    import shutil
    import subprocess
    import os
    from db import configuration
    from util import idtemp_generator
    from util import hoy_string
    from html_helper import grand_button
    from log import log
    from banco import insert_xls_coinag, proceso_xls_coinag
    from gluon import auth
    from gluon import request, session
    from gluon import URL, redirect
    from gluon import H1, H3, H4, I
    from gluon import DIV, FORM, CENTER, TABLE, TR, TAG, INPUT, PRE, XML


@auth.requires_membership('vendedor')
def menu_banco():
    log('acceso')
    # menu favoritos
    form = CENTER(FORM(
        DIV(I(' Carga de Datos', _class='fa fa-ticket fa-2x',
            _id='tit_minigrid'),
            DIV(grand_button('subir xls coinag',
                             URL('tapa14', 'banco', 'xls_coinag'),
                             'fa-file-excel-o'),
                _id='mini_grid'),
            _id='indexdiv'),
        _id='panel_grid'))
    return dict(form=form)


@auth.requires_membership('vendedor')
def xls_coinag():
    form = FORM(
        H1('Carga xls movimientos historicos coinag'),
        TABLE(
            TR(INPUT(_name='farchivos', _type='file', _multiple="multiple")),
            INPUT(_type="submit",
                  _class="btn btn-primary btn-medium")))
    paso1 = CENTER(TABLE(
        form,
        TAG('El/los archivo debe contener las columnas'),
        PRE('Fecha / Hora Mov.\nConcepto\nImporte\nComentarios',
            _id='prestyle')))
    if form.accepts(request, session):
        # me aseguro recibir una lista
        if type(request.vars.farchivos) == list:
            archivos = request.vars.farchivos
        else:
            archivos = [request.vars.farchivos]
        archivos_subidos = []
        path = ('applications/' + str(configuration.get('app.name')) +
                '/files/upload/' + hoy_string() + '/')
        subprocess.run(["mkdir", "-p", path])
        fecha_h = idtemp_generator(4)
        if type(archivos) == list:
            for archivo in archivos:
                nombre = archivo.filename
                contenido = archivo.file
                filename = fecha_h + '_' + nombre
                filepath = path + filename
                shutil.copyfileobj(contenido, open(filepath, 'wb'))
                archivos_subidos.append(filepath)
            log('subidos: ' + str(archivos_subidos))
        session.paso1 = archivos_subidos
        # for archivo in archivos_subidos:
        #    #session.mensaje[archivo] = subo_cbtes(path + archivo)
        #    log(str(archivo))
        # log(str(session.mensaje))
        redirect(URL('visualizacion_xls_coinag'))
    else:
        log('acceso ' + str(request.function))
    return dict(form=paso1)


def visualizacion_xls_coinag():
    visualizaciones = [H3('Previsualizacion planillas')]
    for archivo in session.paso1:
        df = proceso_xls_coinag(archivo)
        # df = pd.read_excel(io=archivo)
        visualizaciones.append(H4(os.path.basename(archivo)))
        visualizaciones.append(
            XML(df.to_html(justify='left',
                           classes='table table-responsive table-striped')))
    paso2 = FORM(CENTER(visualizaciones),
                 CENTER(INPUT(_type="submit",
                              _class="btn btn-primary btn-medium",
                              _value='Procesar',
                              _id='button14')))
    if paso2.accepts(request, session):
        resultado = []
        for archivo in session.paso1:
            insertados, duplicados = insert_xls_coinag(archivo)
            bloque = [H4('Informe'),
                      PRE('archivo' + archivo),
                      H4(insertados),
                      H4('Registros duplicados'),
                      XML(json2html.json2html.convert(duplicados))]
            resultado.extend(bloque)
        session.resultado = resultado
        redirect(URL('resultado_xls_coinag'))
    return dict(form=paso2)


def resultado_xls_coinag():
    return dict(form=FORM(session.resultado))


def xls_coinag_1():
    for archivo in session.paso1:
        log(archivo)
    filet = ('/home/marco/web2py/applications/tapa14/files/upload/2020-12-4/' +
             '2020-12-4_LaBM_COINAG_2020_10.xls')
    df = pd.read_excel(io=filet)
    paso2 = FORM(CENTER(
        XML(df.to_html(justify='left',
                       classes='table table-responsive table-striped'))))
    return dict(form=paso2)
