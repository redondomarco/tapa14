
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import json

# for ide
if 1 == 2:
    import datetime
    import os
    from gluon import auth
    from gluon import redirect, request, response, session
    from gluon import URL, FORM, CENTER, DIV, I, TAG, A, BR, IFRAME
    from gluon import INPUT, SQLFORM, SELECT, H1, H3, H4, H5, H6, HTTP
    from gluon import TABLE, TH, TR, TD, THEAD, TFOOT
    from gluon.validators import IS_NOT_EMPTY, IS_LENGTH
    from db import db, configuration
    from html_helper import grand_button, opt_tabla, select_search
    from funciones import ultimo_comprobante, datos_cliente, datos_productos
    from funciones import get_producto, incremento_comprobante, add_stock
    from funciones import add_reserva, arbol_pedidos, get_listas
    from modelo import fecha_vto
    from funciones import blank_data, restore_backup, agrego_pedido_hdr
    from despacho import proceso_detalle_despacho
    from log import log
    from util import files_dir, hoy_string, idtemp_generator, dict_to_table
    from util import list_dict_to_table_sortable
    from notadeventa import busca_nv, genera_nv, obtengo_pedido
    from notadeventa import test_genera_nv
    from ivalibros import subo_cbtes


@auth.requires_login()
def selec_cliente_pedido():
    clientes = db(db.cliente.is_active is True).select(
        db.cliente.nombre).column('nombre')
    form = FORM(CENTER(
        H4('Seleccione cliente'),
        select_search(clientes, 'nombre'),
        BR(),
        BR(),
        INPUT(_type="submit", _class="btn btn-primary btn-medium",
              _value='Continuar'),
        BR(),
        BR(),
        H5('Utimos pedidos'),
        bloque_utimos_pedidos()
    ))
    if form.accepts(request, session):
        session.cliente = request.vars['seleccion']
        log('seleccionado ' + str(session.cliente))
        redirect(URL('pedido'))
    else:
        log('acceso')
    return dict(form=form)

@auth.requires_membership('vendedor')
def pedido_pendiente():
    log('acceso')
    pedidos = arbol_pedidos()
    # genero elementos grilla
    conjunto_fichas = []
    pedidos_key = []
    for cliente in pedidos.keys():
        total = 0
        d_cliente = datos_cliente(cliente)
        productosficha = []
        pedidos_key.append(list(pedidos[cliente].keys())[0])
        # setpedidos=[]
        for pedido in pedidos[cliente].keys():
            # setpedidos.append(pedido)
            s_pedido = (db.pedidos.pedidonum == int(pedido))
            nota = db(s_pedido).select(db.pedidos.nota).first()['nota']
            productosficha.append(H6('Pedido n°' + str(pedido),
                                     _id='itemficha'))
            productosficha.append(DIV(nota))
            for producto in pedidos[cliente][pedido].keys():
                cantidad = pedidos[cliente][pedido][producto]['cantidad']
                # nota=pedidos[cliente][pedido][producto][1]
                fentrega = pedidos[cliente][pedido][producto]['fentrega']
                total = (int(total) +
                         int(pedidos[cliente][pedido][producto]['total']))
                # total='nada'
                item = (str(cantidad) + ' ' + str(producto) + ' ' +
                        str(fentrega))
                productosficha.append(TR(
                    TD(item, _id='itemficha')))
            idpedido = 'p' + str(pedido)
            productosficha.append(
                TR(TD(DIV(A('Nota de Venta',
                            _href=URL('nota_de_venta',
                                      vars=dict(pedido=pedido)),
                            _class='btn-grid'))))),
            productosficha.append(
                TR(TD(DIV(A('Pago',
                            _href=URL('ingreso_pago',
                                      vars=dict(pedido=pedido)),
                            _class='btn-grid')))))
            productosficha.append(
                TR(TD(DIV(A('Modificar',
                            _href=URL('modifica_pedido',
                                      vars=dict(pedido=pedido)),
                            _class='btn-grid'))),
                   ))
            if 'cta cte' in d_cliente['tipocuenta']:
                productosficha.append(
                    TR(TD(DIV(A('Entregado',
                                _href=URL('finaliza_pedido',
                                          vars=dict(pedido=pedido)),
                                _class='btn-grid')))))
            productosficha.append(
                TR(TD(DIV(INPUT(_id=idpedido, _name=idpedido, _type='number',
                                _min='0', _step='1', _class='cantidad')))))
            productosficha.append(TR(BR()))
            unaficha = DIV(CENTER(
                H5(cliente, _class='gridfont'),
                TABLE(productosficha)),
                BR(),
                DIV('TOTAL $ ' + str(total), _id='aderecha'),
                _class="grid__item js-item")
        conjunto_fichas.append(unaficha)
    # armo div grilla
    grilla = CENTER(DIV(conjunto_fichas, _class="grid"))
    # auxnum.append(pedidonum)
    # pedidonum=set(auxnum)

    nrocomp = str(int(ultimo_comprobante('hoja_de_ruta'))).zfill(10)
    form = FORM(CENTER(
        grilla,
        BR(),
        TABLE(TR(
            TD(TAG('<label class="control-label">Hoja de ruta nº </label>')),
            TD(INPUT(_value=nrocomp, _disabled="disabled",
                     _class="form-control string")),
            TD(INPUT(_type="submit", _class="btn btn-primary btn-medium",
                     _value='Generar', _id='button14'))),
              _id='formventa'),
        BR(), BR(),
        H6('Utimos pedidos'),
        bloque_utimos_pedidos()))
    if form.accepts(request, session):
        log('form aceptado')
        # log('request: ' + str(request.vars))
        hdrnum = ultimo_comprobante('hoja_de_ruta')
        resultado = {'Hoja de Ruta N°': hdrnum}
        lista_pedidos = []
        # log('pedidos_key' + str(pedidos_key))
        for i in pedidos_key:
            idpedido = 'p' + str(i)
            if idpedido in request.vars:
                if request.vars[idpedido] != '':
                    agrego_pedido_hdr(i, hdrnum)
                    lista_pedidos.append(i)
        resultado['pedidos'] = str(lista_pedidos)
        incremento_comprobante('hoja_de_ruta')
        log(resultado)
        session.mensaje = resultado
        redirect(URL('tapa14', 'default', 'mensajes'))
    return dict(form=form)

def hoja_de_ruta():
    log('acceso')
    grid = SQLFORM.smartgrid(
        db.hoja_de_ruta,
        orderby=[~db.hoja_de_ruta.numero],
        searchable=False,
        details=False,
        create=False,
        csv=False)
    form = FORM(CENTER(
        H3('Hoja de ruta'),
        grid,
        A('Limpiar Hojas de Ruta', _href=URL('limpiar_hojas_de_ruta'),
          _class='btn-grid')))
    return dict(form=form)

@auth.requires_membership('vendedor')
def pedido():
    # creo tabla con productos habilitados para el cliente
    idsform = []
    precios = []
    listaflags = []
    d_cliente = datos_cliente(session.cliente)
    d_productos = datos_productos()

    # chequeo que tenga productos habilitados
    if d_cliente['productos'] == []:
        session.mensaje = 'El cliente no tiene productos habilitados'
        redirect(URL('tapa14', 'default', 'mensajes'))

    # genero tabla cabecera
    tabla_cabecera = DIV(H4('Pedido'), DIV(
        DIV(TAG('<label for="clienteinput">Cliente</label>'),
            INPUT(_value=str(session.cliente), _name='cliente',
                  _type='text', _disabled="disabled",
                  _class="form-control string"),),
        DIV(TAG('<label class="control-label">Pedido nº </label>'),
            INPUT(_value=str(int(ultimo_comprobante('pedido'))).zfill(10),
                  _disabled="disabled", _class="form-control string")),
        _id='bloques'),
        DIV(DIV(TAG('<label for="notainput">Nota</label>'),
                INPUT(_name='nota', _type='text', _id="notainput",
                      _class="form-control string")),
            DIV(TAG('<label for="fechaent">Fecha entrega</label>'),
                INPUT(_name='entrega', _type='date', _id="fechaent",
                      _class="form-control string")),
            _id='bloques'))
    # genero tabla para productos habilitados
    t_productos = [THEAD(TR(TH('cant', _id='thpedido'),
                            TH('prod', _id='thpedido'),
                            TH('cod', _id='thpedido'),
                            TH('p.Unit', _id='thpedido'),
                            TH('dto', _id='thpedido'),
                            TH('sub', _id='thpedido')))]

    session.productos = []
    for item in d_cliente['productos']:
        codigo = d_productos[item]['codigo']
        detalle = d_productos[item]['detalle']
        nombre_corto = d_productos[item]['nombre_corto']
        iva_mult = (1 + int(d_cliente['iva_percent']) / 100)
        if d_productos[item]['nombre_lista'] == 'lista':
            v_producto = round(d_productos[item]['valor'], 2)
            listaflags.append(1)
        else:
            v_producto = round(round(d_productos[item]['valor'] *
                                     d_cliente['lista_valor'], 2) *
                               iva_mult, 2)
            listaflags.append(0)
        session.productos.append([codigo, detalle, v_producto])
        idcant = 'c' + codigo
        idvalor = 'v' + codigo
        iddto = 'd' + codigo
        idsubt = 's' + codigo
        t_productos.append(TR(
            TD(INPUT(_id=idcant, _name=idcant, _type='number', _min='0',
                     _step='1', _class='cantidad')),
            TD(nombre_corto),
            TD(codigo, _id=idvalor),
            TD(INPUT(_value=v_producto, _type="number", _class='precio',
                     _disabled="disabled")),
            TD(INPUT(_id=iddto, _name=iddto, _type='number', _min='0',
                     _max='100', _step='any', _class='cantidad')),
            TD(INPUT(_id=idsubt, _name=idsubt, _type="number", _class='precio',
                     _step='any'))))
        idsform.append([idcant, idvalor, iddto, idsubt])
        precios.append(v_producto)
    t_productos.append(TFOOT(TR(
        TH(''), TH(''), TH(''),
        TH(''),
        TH('TOTAL', _id='totaltitle'),
        TH(INPUT(_id='totalt', _type="number", _class='precio',
                 _disabled="disabled")))))
    form = FORM(
        CENTER(tabla_cabecera),
        CENTER(
            DIV(TABLE(
                t_productos, _class='t2', _id="suma"),
                _class='web2py_htmltable',
                _style='width:100%;overflow-x:auto;-ms-overflow-x:scroll'),
            INPUT(_type="submit", _class="btn btn-primary btn-medium",
                  _value='Generar Pedido', _id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        log('pedido aceptado')
        # log(request.vars)
        # pedido
        s_pedido = (db.comprobante.nombre == 'pedido')
        pedidonumactual = db(s_pedido).select()[0].lastid
        # cliente
        s_cliente = (db.cliente.nombre == session.cliente)
        listaid = db(s_cliente).select().first()['lista']
        # valor lista
        v_lista = db(db.listas.id == listaid).select().first()['valor']
        # capturo nota
        nota = request.vars.nota
        # log(str(request.vars.entrega))
        if request.vars.entrega != "":
            fentrega = datetime.strptime(
                request.vars.entrega.replace('/', '-') + ' 12:00:00',
                '%Y-%m-%d %H:%M:%S')
        else:
            # poner fentrega today+1
            fentrega = request.vars.entrega
        log('f_entrega: ' + fentrega + ' - nota: ' + str(nota))
        # log(request.vars)
        resultado = {'cliente': session.cliente,
                     'n° pedido': pedidonumactual,
                     'nota': nota,
                     'fecha entrega': fentrega,
                     'total': 0
                     }
        for item in d_cliente['productos']:
            producto = db(db.producto.id == item).select().first()
            cant = 'c' + str(item.codigo)
            dto = 'd' + str(item.codigo)
            tot = 's' + str(item.codigo)
            if request.vars[cant] == '':
                cantidad = int(0)
            else:
                cantidad = int(str(request.vars[cant]))
            # saco descuento del request
            if request.vars[dto] == '':
                descuento = float(0)
            else:
                descuento = float(str(request.vars[dto]))
            # deberia siempre traer al menos un cero, valido igual
            if request.vars[tot] == '':
                total = int(0)
            else:
                total = float(str(request.vars[tot]))
            if cantidad != 0:
                # logica descuento stock
                if producto['stock_alias'] is None:
                    # no es un alias
                    codigo = item
                else:
                    # es un alias, obtengo el producto real
                    codigo = get_producto(producto['stock_alias'])['id']
                # finalmente resto el stock
                add_stock(item, -cantidad)
                # lo sumo a reserva
                add_reserva(codigo, cantidad)
                valor = float(producto['valor'])
                detalle = producto['detalle']
                productoid = producto['id']
                s_mail = (db.auth_user.email == auth.user.email)
                vendedorid = db(s_mail).select().first()['id']
                s_name = (db.cliente.nombre == session.cliente)
                clienteid = db(s_name).select().first()['id']
                listaid = db(s_name).select().first()['lista']
                preciou = round(valor * v_lista, 2)
                # el total ahora lo traigo del form
                # total = round(preciou * int(cantidad) *
                #             ((100 - descuento) / 100), 2)
                log(' #' + str(pedidonumactual) +
                    ' cant ' + str(cantidad) +
                    ' dto ' + str(descuento) +
                    ' ' + str(detalle) +
                    ' pu ' + str(preciou) +
                    ' total ' + str(total) +
                    ' cli ' + str(session.cliente))
                db.pedidos.insert(
                    fecha=datetime.datetime.now(),
                    fentrega=fentrega,
                    pedidonum=pedidonumactual,
                    vendedor=vendedorid,
                    cliente=clienteid,
                    nota=str(nota),
                    cantidad=int(cantidad),
                    descuento=int(descuento),
                    producto=productoid,
                    preciou=preciou,
                    total=total
                )
                prod_show = (str(cantidad) + ' ' + str(detalle) + ' ' +
                             str(total))
                clave_show = '~item' + str(item)
                resultado[clave_show] = prod_show
                resultado['total'] += total
        # aumento cuenta nro pedido3
        incremento_comprobante('pedido')
        session.mensaje = resultado
        log(resultado)
        redirect(URL('tapa14', 'default', 'mensajes'))
    else:
        log('acceso')
    # log(str(idsform))
    return dict(form=form, ids_json=json.dumps(idsform),
                listas_json=json.dumps(get_listas()),
                iva_percent=int(d_cliente['iva_percent']),
                precios_json=json.dumps(precios),
                listaflags_json=json.dumps(listaflags))


@auth.requires_membership('vendedor')
def nota_de_venta():
    pedidonum = request.vars['pedido']
    log('solicitud NV: ' + str(pedidonum))
    # busco si ya esta generada
    busqueda = busca_nv('nv_' + str(pedidonum) + '.pdf')
    if busqueda[0] == 'ok':
        log('encontrado: archivo' + str(busqueda[1][25:]))
        session.nvurl = URL('tapa14','default','archivo' + str(busqueda[1][25:]))
        redirect(URL('muestra_nv'))
    pedido = obtengo_pedido(pedidonum)
    hoy = datetime.datetime.now()
    fecha = str(hoy.day) + '/' + str(hoy.month) + '/' + str(hoy.year)
    clienteid = pedido['cliente_id']
    if pedido['fentrega'] is None:
        nota = pedido['nota']
    else:
        fechanota = str(pedido['fentrega'].day) + '/' + str(pedido[1].month)
        nota = pedido['nota'] + ' ' + fechanota
    items = pedido['productos']
    # directorio='applications/dev/pdf/2018/6/19/nv/'
    directorio = (files_dir + 'pdf/' + str(hoy.year) + '/' + str(hoy.month) +
                  '/' + str(hoy.day) + '/nv/')
    urlfile = ('tapa14/default/archivo/pdf/' + str(hoy.year) + '/' + str(hoy.month) + '/' +
               str(hoy.day) + '/nv/nv_' + str(pedidonum) + '.pdf')
    log(urlfile)
    session.nvurl = URL(urlfile)
    log('debug ' + str(session.nvurl))
    try:
        os.makedirs(directorio)
    except Exception:
        pass
    pathnv = genera_nv(fecha, pedidonum, clienteid, items, directorio, nota)
    log(pathnv)
    redirect(URL('muestra_nv'))


def muestra_nv():
    # pdfexample=test_genera_nv()
    # mostrar=Expose('/home/marco/web2py/'+pdfexample)
    files = CENTER(
        # DIV(A('test_nv',_class="btn btn-primary", _href=URL('test_nv'))),
        # DIV(IFRAME(_src=session.nvurl, _width="630px", _height='891'))
        DIV(IFRAME(_src=session.nvurl,
                   _id='verpdf',
                   # _style="width:630px; height:500px;",
                   )),
        TABLE(TR(
            TD(A('Volver', _href=request.env.http_referer, _class='btn btn-primary btn-medium')),
            TD(H6('Nota de venta: ' + str(session.nvurl))))),
    )
    return dict(files=files)

def bloque_utimos_pedidos():
    ult_pedidos = SQLFORM.grid(
        db.pedidos,
        fields=[db.pedidos.fecha, db.pedidos.pedidonum, db.pedidos.vendedor,
                db.pedidos.cliente, db.pedidos.cantidad, db.pedidos.producto,
                db.pedidos.total],
        headers={db.pedidos.pedidonum: 'n'},
        orderby=[~db.pedidos.fecha],
        searchable=False,
        editable=False,
        deletable=False,
        create=False,
        sortable=True,
        details=False,
        paginate=30,
        csv=False,
        maxtextlength=30,)
    return(ult_pedidos)