# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import subprocess
import shutil
import json
from gluon.tools import Expose
# for ide
if False:
    from gluon import *
    from html_helper import grand_button, opt_tabla
    from funciones import ultimo_comprobante, datos_cliente, datos_productos
    from funciones import get_producto, incremento_comprobante, add_stock
    from funciones import add_reserva
    from modelo import fecha_vto
    from log import log


@auth.requires_login()
def index():
    # router de pantalla inicial
    log('acceso ' + str(request.function))
    if hasattr(auth.user, 'email'):
        usuario = str(auth.user.email)
        if usuario == 'oficina.tapa14@gmail.com':
            redirect(URL('index_data_entry'))
        else:
            redirect(URL('index_todo'))
    return dict()


@auth.requires_membership('oficina_data_entry')
def index_data_entry():
    form = CENTER(FORM(
        DIV(I(' Contabilidad', _class='fa fa-calculator fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('Caja',
                             URL('tapa14', 'contable', 'consulta_caja'),
                             'fa-dollar'),
                grand_button('Cuentas',
                             URL('tapa14', 'contable', 'entry_tabla',
                                 vars={'tabla': 'tipos_cuenta'}),
                             'fa-list'),
                grand_button('Personas',
                             URL('tapa14', 'contable', 'entry_tabla',
                                 vars={'tabla': 'personas'}),
                             'fa-users'),
                _id='mini_grid'),
            _id='indexdiv'),
        _id='panel_grid'))
    return dict(form=form)


@auth.requires_membership('vendedor')
def index_todo():
    log('acceso')
    # menu favoritos
    form = CENTER(FORM(
        DIV(I(' Ventas', _class='fa fa-ticket fa-2x',
            _id='tit_minigrid'),
            DIV(grand_button('nuevo pedido',
                             URL('tapa14', 'default', 'selec_cliente_pedido'),
                             'fa-cart-plus'),
                grand_button('pedidos pendientes',
                             URL('tapa14', 'default', 'pedido_pendiente'),
                             'fa-th-large'),
                grand_button('hoja de ruta',
                             URL('tapa14', 'default', 'hoja_de_ruta'),
                             'fa-truck'),
                grand_button('Ingreso Pago',
                             URL('tapa14', 'default', 'pago'),
                             'fa-paypal'),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Produccion', _class='fa fa-industry fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('ingreso productos terminados',
                             URL('tapa14', 'default', 'ingreso_produccion'),
                             'fa-database'),
                grand_button('consulta productos',
                             URL('tapa14', 'default',
                                 'consulta_ingreso_stock'),
                             'fa-list'),
                grand_button('Ingreso materias primas',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'mat_primas'}),
                             'fa-qrcode'),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Compras', _class='fa fa-shopping-bag fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('ingreso productos terminados',
                             URL('tapa14', 'default', 'ingreso_produccion'),
                             'fa-database'),
                grand_button('consulta productosNN',
                             'consulta_ingreso_stock',
                             'fa-list'),
                grand_button('Ingreso materias primasNN',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'mat_primas'}),
                             'fa-qrcode'),
                _id='mini_grid'),
            _id='indexdiv'),
        DIV(I(' Contabilidad', _class='fa fa-calculator fa-2x',
              _id='tit_minigrid'),
            DIV(grand_button('Caja',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'caja'}),
                             'fa-dollar'),
                grand_button('EgresosNN',
                             URL('tapa14', 'default',
                                 'consulta_ingreso_stock'),
                             'fa-upload'),
                grand_button('ConsultaNN',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'mat_primas'}),
                             'fa-university'),
                grand_button('mov Caja',
                             URL('tapa14', 'contable', 'mov_caja_sel_fecha'),
                             'fa-upload'),
                _id='mini_grid'),
            _id='indexdiv'),
        _id='panel_grid'))
    return dict(form=form)


def admin():
    log('acceso')
    form = CENTER(FORM(
        DIV(I(' Tapa14', _class='fa fa-cogs fa-2x'),
            DIV(grand_button('modificar productos',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'producto'}),
                             'fa-product-hunt'),
                grand_button('materias primas',
                             URL('tapa14', 'default', 'admin_tabla',
                                 vars={'tabla': 'mat_primas'}),
                             'fa-leaf'),
                grand_button('Personas',
                             URL('tapa14', 'contable', 'entry_tabla',
                                 vars={'tabla': 'personas'}),
                             'fa-users'),
                grand_button('Cuentas',
                             URL('tapa14', 'contable', 'entry_tabla',
                                 vars={'tabla': 'tipos_cuenta'}),
                             'fa-list'),
                _id='mini_grid'),
            ),
        DIV(I(' Clientes', _class='fa fa-cogs fa-2x'),
            DIV(grand_button('modificar clientes',
                             'admin_tabla',
                             'fa-users',
                             vars={'tabla': 'cliente'}),
                grand_button('listas de precios',
                             'admin_tabla',
                             'fa-percent',
                             vars={'tabla': 'listas'}),
                _id='mini_grid')
            ),
        DIV(I(' Proveedores', _class='fa fa-cogs fa-2x'),
            DIV(grand_button('Proveedores',
                             'admin_tabla',
                             'fa-suitcase',
                             vars={'tabla': 'proveedor'}),
                grand_button('tipo materias primas',
                             'admin_tabla',
                             'fa-puzzle-piece',
                             vars={'tabla': 'tipos_mat_primas'}),
                grand_button('marcas',
                             'admin_tabla',
                             'fa-trademark',
                             vars={'tabla': 'marcas'}),
                _id='mini_grid')
            ),
        DIV(I(' Anula', _class='fa fa-cogs fa-2x'),
            DIV(grand_button('pedido',
                             'admin_tabla',
                             'fa-window-close-o',
                             vars={'tabla': 'marcas'}),
                _id='mini_grid')
            ),
        _id='panel_grid'))
    return dict(form=form)


@auth.requires_login()
@auth.requires_membership('admin')
def admin_tabla():
    if 'tabla' in request.vars:
        tabla = request.vars['tabla']
        titulo = DIV(
            # A(icon_title('fa-arrow-left', 'Volver'), _id='boton_r',
            #   _class="btn-grid", _href=URL('admin')),
            CENTER(H4('Admin ' + (str(tabla).title()))))
        log('acceso grid ' + str(tabla))
        grid = SQLFORM.smartgrid(eval('db.' + str(tabla)),
                                 maxtextlength=20,
                                 linked_tables=['child'],
                                 fields=eval(opt_tabla(tabla)['fields']))
        return dict(grid=grid, titulo=titulo)
    else:
        redirect(URL('index'))


@auth.requires_membership('vendedor')
def ingreso_produccion():
    log('acceso')
    # armo cabecera de datos fecha, lote, maquina, harina, margarina,
    # sal, conservantes
    cabecera = DIV(CENTER(
        DIV(TAG('<label for="fecha_p">Fecha Produccion</label>'),
            INPUT(_name='ffechap', _type='date', _id="fechap",
                  _class="form-control string",
                  requires=IS_NOT_EMPTY())),
        DIV(TAG('<label class="control-label">Hoja nº </label>'),
            INPUT(_value=str(int(ultimo_comprobante('ingreso'))).zfill(10),
                  _disabled="disabled", _class="form-control string")),
        DIV(TAG('<label for="lote"> Lote </label>'),
            INPUT(_name='flote', _type='number',
                  _min='1', _max='365', _id='lote',
                  _class="form-control string")),
        DIV(TAG('<label for="fecha_p">Fecha Vencimiento</label>'),
            INPUT(_name='ffechav', _type='date', _id="fechap",
                  _class="form-control string")),
        DIV(TAG('<label for="fecha_p">Lote Harina</label>'),
            SELECT(['a', 'b'], _name='fharina', _id="fharina",
                   _class="form-control string")),
        DIV(TAG('<label for="notainput">Nota</label>'),
            INPUT(_name='nota', _type='text', _id="notainput",
                  _class="form-control string"), _id="ancho190"),
        _id='bloques'))
    # armo ultimos ingresos
    ultimosingresos = SQLFORM.grid(
        db.ingresos,
        fields=(db.ingresos.fecha, db.ingresos.lote,
                db.ingresos.usuario, db.ingresos.cantidad,
                db.ingresos.producto),
        orderby=[~db.ingresos.fecha],
        searchable=False, editable=False, deletable=False, create=False,
        sortable=True, details=False, maxtextlength=25)
    session.productos = []
    session.idsform = []
    tabla1 = [[THEAD(TR(TH('cant'), TH('det'), TH('fis'), TH('net')))]]
    prod_real = db(db.producto.stock_alias is None and
                   db.producto.tipo == 'propio').select()
    for item in prod_real:
        session.productos.append([item.codigo,
                                  item.nombre_corto,
                                  item.valor,
                                  item.stock])
        tabla1.append(TR(
            TD(INPUT(_name='c' + str(item.codigo),
                     _type='number', _min='0', _step='1', _class='cantidad')),
            TD(item.nombre_corto),
            TD(item.stock),
            TD(item.reserva)))
# TD(item.valor, _id='v'+str(item.codigo)),
# TD(INPUT(_id='s'+str(item.codigo), _type="number",_class='precio',
#    _disabled="disabled"))))
        session.idsform.append(['c' + str(item.codigo),
                                'v' + str(item.codigo),
                                's' + str(item.codigo)])
    # tabla1.append(TFOOT(TR(TH(''), TH(''), TH(''),
    #    TH('Total',_id='totaltitle'),
    #    TH(INPUT(_id='totalt', _type="number",_class='precio',
    #      _disabled="disabled")))))
    # formulario
    form_ingreso = FORM(
        CENTER(
            H3('Ingreso de producción'),
            cabecera,
            TABLE(tabla1, _class='t2', _id="suma"),
            TABLE(TR(A('Volver', _href=request.env.http_referer,
                  _class='btn btn-primary btn-medium'),
                  INPUT(_type="submit", _class="btn btn-primary btn-medium",
                        _value='Ingresar', _id='button14')))))
    if form_ingreso.accepts(request, session):
        for item in db(db.producto.codigo).select():
            cant = 'c' + str(item.codigo)
            if request.vars['ingresofecha'] != '':
                log(request.vars['ingresofecha'])
                ingresofecha = datetime.datetime.strptime(request.vars['ingresofecha'].replace('/', '-') + ' 12:00:00', '%d-%m-%Y %H:%M:%S')
                debug(type(ingresofecha))
            else:
                ingresofecha = ''
            ingresolote = request.vars['ingresolote']
            fechavto = fecha_vto(ingresolote)
            debug(type(fecha_vto(ingresolote)))
            cantidad = request.vars[cant]
            if cantidad == '' or cantidad is None:
                cantidad = int(0)
            selector = (db.producto.codigo == item.codigo)
            stock = db(selector).select()[0].stock
            if stock is not None:
                db(selector).update(
                    stock=db(selector).select()[0].stock + int(cantidad))
            else:
                db(selector).update(stock=int(cantidad))
            if cantidad != 0:
                log(str(cantidad) + ' ' + str(item.codigo) + ' desde ' +
                    str(request.client) + ' fecha ' +
                    str(ingresofecha) + ' lote ' + str(ingresolote))
                s_producto = (db.producto.codigo == item.codigo)
#                producto = db(s_producto).select().first()['detalle']
                productoid = db(s_producto).select().first()['id']
                db.ingresos.insert(
                    fecha=datetime.datetime.now(),
                    fecha_prod=ingresofecha,
                    lote=ingresolote,
                    vto=fechavto,
                    usuario=auth.user.email,
                    cantidad=cantidad,
                    producto=productoid)
        db.commit()
        redirect(URL('index'))
    else:
        log('acceso')
    return dict(form_ingreso=form_ingreso,
                ids_json=json.dumps(session.idsform),
                ultimosingresos=ultimosingresos
                )


# armo tabla de productos para venta y calculadora
session.productos = []
session.idsform = []
tabla1 = [THEAD(TR(TH('cant'), TH('detalle'),
                   TH('stock'), TH('final'), TH('sub')))]
for item in db(db.producto.detalle).select():
    session.productos.append([item.codigo, item.detalle,
                              item.valor, item.stock])
    tabla1.append(TR(
        TD(INPUT(_id='c' + str(item.codigo), _name='c' + str(item.codigo),
                 _type='number', _min='0', _step='1', _class='cantidad')),
        TD(item.detalle),
        TD(item.stock),
        TD(item.valor, _id='v' + str(item.codigo)),
        TD(INPUT(_id='s' + str(item.codigo), _type="number", _class='precio',
                 _disabled="disabled"))))
    session.idsform.append(['c' + str(item.codigo), 'v' + str(item.codigo),
                           's' + str(item.codigo)])
tabla1.append(TFOOT(TR(
    TH(''), TH(''), TH(''),
    TH('Total', _id='totaltitle'),
    TH(INPUT(_id='totalt', _type="number", _class='precio',
             _disabled="disabled")))))


@auth.requires_membership('vendedor')
def ventaold():
    clientes = db(db.cliente).select(db.cliente.ALL)
    listas = db(db.listas).select(db.listas.ALL)
    selector = (db.comprobante.nombre == 'venta')
    comprobante = db(selector).select().first()['lastid']
    log("tabla1: " + str(tabla1))
    form_venta = FORM(CENTER(
        TABLE(TR(TAG('<label for="clienteinput">cliente</label>'),
              SELECT([" "] + [(p.nombre) for p in clientes], _name='cliente',
                     _type='text', _id="clienteinput",
                     _class="form-control string"),
              TAG('<label class="control-label">Venta nº </label>'),
              INPUT(_value=str(int(comprobante)).zfill(10),
                    _disabled="disabled", _class="form-control string",
                    _id='nrocomp')),
              _id='tablacliente'),),
        TABLE(tabla1, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium",
                     _value='vender', _id='button14')),
        _id='formventa')
    if form_venta.accepts(request, session):
        log('aceptado')
        cliente = request.vars['cliente']
        if cliente == " ":
            log('cliente vacio ' + str(cliente))
            redirect(URL('index'))
        else:
            log('cliente:' + str(cliente))
        s_venta = (db.comprobante.nombre == 'venta')
        ventanumactual = db(s_venta).select()[0].lastid
        listaid = db(db.cliente.nombre == cliente).select().first()['lista']
#        desc_lista = db(db.listas.id == listaid).select().first()['valor']
        for item in db(db.producto.detalle).select():
            cant = 'c' + str(item.codigo)
#            cantidad=int(str(request.vars[cant]))
            if request.vars[cant] == '':
                cantidad = int(0)
            else:
                cantidad = int(str(request.vars[cant]))
            s_codigo = (db.producto.codigo == item.codigo)
            db(s_codigo).update(stock=db(s_codigo).select()[0].stock -
                                int(cantidad))
            if cantidad != 0:
                s_codigo = (db.producto.codigo == item.codigo)
                s_email = (db.auth_user.email == auth.user.email)
                s_nombre = (db.cliente.nombre == cliente)
                s_lista = (db.listas.id == listaid)
                valor = float(db(s_codigo).select().first()['valor'])
                producto = db(s_codigo).select().first()['detalle']
                productoid = db(s_codigo).select().first()['id']
                vendedorid = db(s_email).select().first()['id']
                clienteid = db(s_nombre).select().first()['id']
                listaid = db(s_nombre).select().first()['lista']
                descuento = float(db(s_lista).select().first()['valor'])
                preciou = round(valor * descuento, 2)
                total = preciou * int(cantidad)
                log('venta #' + str(ventanumactual) + ' cant ' +
                    str(cantidad) + ' ' + str(producto) + ' pu ' +
                    str(preciou) + ' total ' + str(total) + ' a ' +
                    str(cliente))
                db.ventas.insert(
                    fecha=datetime.datetime.now(),
                    vendedor=vendedorid,
                    cliente=clienteid,
                    ventanum=ventanumactual,
                    cantidad=int(cantidad),
                    producto=productoid,
                    preciou=preciou,
                    total=total
                )
        s_comprobante = (db.comprobante.nombre == 'venta')
        db(s_comprobante).update(lastid=db(s_comprobante).select()[0].lastid +
                                 1)
        db.commit()
        redirect(URL('index'))
    else:
        log('acceso')
    return dict(form_venta=form_venta, ids_json=json(session.idsform),
                clientes_json=json(clientes), listas_json=json(listas))


def selec_cliente_pedido():
    clientes = db(db.cliente.is_active is True).select(db.cliente.ALL)
    form = FORM(CENTER(
        H4('Pedido'),
        BR(),
        TAG('<label for="clienteinput">Cliente</label>'),
        SELECT([" "] + [(p.nombre) for p in clientes], _name='cliente',
               _type='text', _id="clienteinput",
               _class="form-control string"),
        BR(),
        INPUT(_type="submit", _class="btn btn-primary btn-medium",
              _value='Continuar')
    ))
    if form.accepts(request, session):
        session.cliente = request.vars['cliente']
        log('seleccionado ' + str(session.cliente))
        redirect(URL('pedido'))
    else:
        log('acceso')
    return dict(form=form)


@auth.requires_membership('vendedor')
def pedido():
    # creo tabla con productos habilitados para el cliente
    idsform = []
    precios = []
    d_cliente = datos_cliente(session.cliente)
    d_productos = datos_productos()

    # chequeo que tenga productos habilitados
    if d_cliente['productos'] == []:
        session.mensaje = 'El cliente no tiene productos habilitados'
        redirect(URL('mensajes'))

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
        v_producto = round(d_productos[item]['valor'] *
                           d_productos[item]['lista_valor'] *
                           d_cliente['lista_valor'] *
                           (1 + int(d_cliente['iva_percent']) / 100), 3)
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
        redirect(URL('mensajes'))
    else:
        log('acceso')
    # log(str(idsform))
    return dict(form=form, ids_json=json.dumps(idsform),
                listas_json=json.dumps(listasp()),
                iva_percent=int(d_cliente['iva_percent']),
                precios_json=json.dumps(precios))


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
        paginate=20,
        csv=False,
        maxtextlength=30,)
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
        TAG('Ultimos Pedidos'),
        ult_pedidos))
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
        redirect(URL('mensajes'))
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


def limpiar_hojas_de_ruta():
    db.hoja_de_ruta.truncate()
    db.commit()
    redirect(URL('hoja_de_ruta'))


# def modifica_pedido():
#    numero_pedido = request.vars['pedido']
#    sel_pedido = (db.pedidos.pedidonum == numero_pedido)
#    pedido_dict = db(sel_pedido).select().as_dict()


def anula_pedido():
    log('acceso')
    grid = SQLFORM.smartgrid(
        db.pedidos)
    return locals()
    # ingreso pedido


@auth.requires_membership('vendedor')
def nota_de_venta():
    pedidonum = request.vars['pedido']
    log('solicitud NV: ' + str(pedidonum))
    # busco si ya esta generada
    busqueda = busca_nv('nv_' + str(pedidonum) + '.pdf')
    if busqueda[0] == 'ok':
        log('encontrado: archivo' + str(busqueda[1][25:]))
        session.nvurl = URL('archivo' + str(busqueda[1][25:]))
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
    urlfile = ('archivo/pdf/' + str(hoy.year) + '/' + str(hoy.month) + '/' +
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
        H6('Nota de venta: ' + str(session.nvurl)),
        # DIV(A('test_nv',_class="btn btn-primary", _href=URL('test_nv'))),
        # DIV(IFRAME(_src=session.nvurl, _width="630px", _height='891'))
        DIV(IFRAME(_src=session.nvurl, _id='verpdf'))
    )
    return dict(files=files)


@auth.requires_membership('vendedor')
def finaliza_pedido():
    pedidos = db(db.pedidos.pedidonum == session.pedido).select().as_dict().values()
    session.clienteid = pedidos[0]['cliente']
    session.cliente = db(db.cliente.id == session.clienteid).select().first()['nombre']
    listas = db(db.listas).select(db.listas.ALL)
    comprobante = db(db.comprobante.nombre == 'venta').select().first()['lastid']
    session.ultimasventas = SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha, db.ventas.ventanum, db.ventas.vendedor,
                db.ventas.cliente, db.ventas.cantidad, db.ventas.producto,
                db.ventas.total),
        orderby=[~db.ventas.fecha], searchable=False, editable=False, deletable=False, create=False, sortable=True, details=False, maxtextlength=25)
    # creo tabla con productos habilitados para el cliente
    session.productos = []
    idsform = []
    precios = []
    productos_cliente = db(db.cliente.nombre == session.cliente).select().first()['productos']
    idtipocuenta = db(db.cliente.nombre == session.cliente).select().first()['tipocuenta']
    if idtipocuenta is not None:
        tipocuenta = db(db.tipo_cta.id == idtipocuenta).select().first()['tipo']
    else:
        session.mensaje = 'El cliente no tiene tipo de cuenta valida'
        redirect(URL('mensajes'))
    listaidcliente = db(db.cliente.nombre == session.cliente).select().first()['lista']
    descuento = db(db.listas.id == listaidcliente).select().first()['valor']
    if productos_cliente is not None:
        session.mensaje = 'El cliente no tiene productos habilitados'
        redirect(URL('mensajes'))
    nro_venta = TR(TAG('<label class="tabla-label">Venta nº </label>'),
                   INPUT(_value=str(int(comprobante)).zfill(10),
                         _disabled="disabled", _id='nrocomp'))
    nombre_cliente = TR(TAG('<label for="clienteinput">cliente</label>'),
                        INPUT(_value=str(session.cliente),
                              _name='cliente', _disabled="disabled",
                              _type='text', _id="clienteinput"))
    tipo_cuenta = TR(TAG('<label for="tipocuenta">cuenta</label>'),
                     INPUT(_value=str(tipocuenta), _name='tipocuenta',
                           _disabled="disabled", _type='text', _id="tipocuenta"))
    if tipocuenta == 'efectivo':
        tablacliente = TABLE(nro_venta,
                             nombre_cliente,
                             tipo_cuenta,
                             _id='tablacliente')
    elif tipocuenta == 'cta cte':
        saldo_cliente = db(db.cliente.nombre == session.cliente).select().first()['saldo']
        if saldo_cliente < 0:
            tagid = 'saldonegativo'
        else:
            tagid = 'tipocuenta'
        saldo = TR(TAG('<label for="tipocuenta">saldo</label>'),
                   INPUT(_value=str(saldo_cliente), _disabled="disabled",
                         _type="number", _class=tagid))
        if session.entrega == 'Inmediata':
            fechaentrega = ""
        elif session.entrega == "Posterior":
            fecha_entrega = TR(TAG('<label class="tabla-label">Entrega: </label>'),
                               INPUT(_class='date', _name='fechaentrega', _id='fechaingreso'))
        tablacliente = TABLE(nro_venta,
                             nombre_cliente,
                             tipo_cuenta,
                             saldo,
                             _id='tablacliente')
    else:
        session.mensaje = 'El cliente no tiene tipo de cuenta valida'
        redirect(URL('mensajes'))
    # genero tabla para form
    tabla2 = []
    tabla2.append(THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'), TH('sub'))))
    for item in productos_cliente:
        #
        # for uno in pedidos:
        #    if
        #
        producto = db(db.producto.id == item).select().first()
        session.productos.append([producto['codigo'],
                                  producto['detalle'],
                                  producto['valor']])
        tabla2.append(TR(
            TD(INPUT(_id='c' + str(producto['codigo']),
                     _name='c' + str(producto['codigo']),
                     _type='number', _min='0', _step='1',
                     _class='cantidad')),
            TD(producto['detalle']),
            TD(producto['codigo'], _id='v' + str(producto['codigo'])),
            TD(INPUT(_id='s' + str(producto['codigo']), _type="number", _class='precio', _disabled="disabled"))))
        idsform.append(['c' + str(producto['codigo']),
                        'v' + str(producto['codigo']),
                        's' + str(producto['codigo'])])
        precios.append(producto['valor'])
    tabla2.append(TFOOT(TR(
        TH(''), TH(''), TH('Total', _id='totaltitle'), TH(INPUT(_id='totalt', _type="number", _class='precio', _disabled="disabled")))))
    form = FORM(
        CENTER(tablacliente),
        TABLE(tabla2, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium",
                     _value='vender', _id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        productovendido = False
        log('aceptado')
        ventanumactual = db(db.comprobante.nombre == 'venta').select()[0].lastid
        listaid = db(db.cliente.nombre == session.cliente).select().first()['lista']
        desc_lista = db(db.listas.id == listaid).select().first()['valor']
        for item in productos_cliente:
            producto = db(db.producto.id == item).select().first()
            cant = 'c' + str(item.codigo)
            if request.vars[cant] == '':
                cantidad = int(0)
            else:
                cantidad = int(str(request.vars[cant]))
            if cantidad != 0:
                productovendido = True
                # logica descuento stock
                if producto['stock_alias'] is None:
                    selprod = (db.producto.codigo == producto['codigo'])
                    db(selprod).update(stock=db(selprod).select()[0].stock - int(cantidad))
                else:
                    stockprod = db(db.producto.id == producto['stock_alias']).select().first()
                    prod_cod = (db.producto.codigo == stockprod['codigo'])
                    db(prod_cod).update(stock=db(prod_cod).select()[0].stock - int(cantidad))
                valor = float(producto['valor'])
                detalle = producto['detalle']
                productoid = producto['id']
                vendedorid = db(db.auth_user.email == auth.user.email).select().first()['id']
                clienteid = db(db.cliente.nombre == session.cliente).select().first()['id']
                listaid = db(db.cliente.nombre == session.cliente).select().first()['lista']
                preciou = round(valor * descuento, 2)
                total = preciou * int(cantidad)
                log(f'venta #{ventanumactual} cant {cantidad} {detalle} '
                    f'pu {preciou} total {total} a {session.cliente}')
                db.ventas.insert(
                    fecha=datetime.now(),
                    vendedor=vendedorid,
                    cliente=clienteid,
                    ventanum=ventanumactual,
                    cantidad=int(cantidad),
                    producto=productoid,
                    preciou=preciou,
                    total=total
                )
        # solo subo el numero de venta si no fue todo 0
        if productovendido:
            operacion = (db.comprobante.nombre == 'venta')
            db(operacion).update(
                lastid=db(operacion).select()[0].lastid + 1)
        db.commit()
        redirect(URL('index'))
    else:
        log(str(session.cliente) + ' ingreso')
    return dict(form=form, ids_json=json(idsform),
                listas_json=json(listas), descuento=descuento,
                precios_json=json(precios))


@auth.requires_membership('admin')
def clientes():
    log('acceso admin')
    grid = SQLFORM.grid(
        db.cliente,
        maxtextlength=25,
        fields=(db.cliente.nombre, db.cliente.lista, db.cliente.saldo,
                db.cliente.tipocuenta)
    )
    return locals()


@auth.requires_membership('productor')
def consulta_ingreso_stock():
    log('ingreso')
    grid = SQLFORM.smartgrid(
        db.ingresos,
        fields=(db.ingresos.fecha, db.ingresos.usuario,
                db.ingresos.cantidad, db.ingresos.producto,
                db.ingresos.lote),
        searchable=True, editable=False, deletable=False, create=False,
        sortable=True, details=True, maxtextlength=25)
    return locals()


@auth.requires_membership('vendedor')
def consulta_venta_stock():
    log('ingreso')
    grid = SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha,
                db.ventas.ventanum,
                db.ventas.vendedor,
                db.ventas.cliente,
                db.ventas.cantidad,
                db.ventas.producto,
                db.ventas.preciou,
                db.ventas.total),
        searchable=True,
        editable=False,
        deletable=False,
        create=False,
        sortable=True,
        details=False,
        maxtextlength=25)
    return locals()


@auth.requires_membership('vendedor')
def consulta_stock():
    log('ingreso')
    grid = SQLFORM.grid(db.producto,
                        fields=(db.producto.codigo, db.producto.detalle,
                                db.producto.valor, db.producto.stock),
                        searchable=True,
                        editable=False,
                        deletable=False,
                        create=False,
                        sortable=True,
                        details=False,
                        maxtextlength=25)
    return locals()


def test_nv():
    pdfexample = test_genera_nv()
    log(pdfexample)
    session.nvurl = URL('archivo/pdf/test/nv/nv_19.pdf')
    redirect(URL('muestra_nv'))


@auth.requires_login()
@auth.requires_membership('vendedor')
def archivo():
    expose = ('applications/' + str(configuration.get('app.name')) +
              '/files')

    subprocess.run(["mkdir", "-p", expose])
    return dict(files=Expose(expose, extensions=['.csv', '.pdf', '.txt']))


def mensajes():
    if isinstance(session.mensaje, dict):
        tabla = dict_to_table(session.mensaje, id='tablaresult')
        aceptar = A('Aceptar', _id='boton_r',
                    _class="btn-grid",
                    _href=URL('index'))
        titulo = H4('Resultado')
        contenido = CENTER(titulo, tabla, aceptar)
    elif isinstance(session.mensaje, str):
        log('muestro: ' + str(session.mensaje))
        contenido = session.mensaje
    elif isinstance(session.mensaje, DIV):
        contenido = session.mensaje
    else:
        contenido = 'error en mensaje'
    return dict(contenido=contenido)


def capture_update():
    log(request.vars.data)
#    return db().insert(data = request.vars.data)


# ---- API (example) -----


# @auth.requires_login()
# def api_get_user_email():
#     if not request.env.request_method == 'GET': raise HTTP(403)
#     return response.json({'status': 'success', 'email': auth.user.email})

# ---- Smart Grid (example) -----


# @auth.requires_membership('admin')
# def grid():
#     response.view = 'generic.html'  # use a generic view
#     tablename = request.args(0)
#     if (not tablename in db.tables):
#         raise HTTP(403)
#     grid = SQLFORM.smartgrid(db[tablename], args=[tablename],
#                              deletable=False, editable=False)
#     return dict(grid=grid)

# ---- Embedded wiki (example) ----
# def wiki():
#    auth.wikimenu() # add the wiki to the menu
#    return auth.wiki()


# def subir_datos_afip_paso1():
#     session.paso1 = []
#     form = FORM(
#         H1('Ingrese archivos cabecera zip afip'),
#         TABLE(
#             TR(INPUT(_name='archivo1', _type='file',
#                      requires=IS_LENGTH(1048576, 8))),
#             TR(INPUT(_name='archivo2', _type='file',
#                      requires=IS_LENGTH(1048576, 8))),
#             TR(INPUT(_name='archivo3', _type='file',
#                      requires=IS_LENGTH(1048576, 8))),
#             TR(INPUT(_name='archivo4', _type='file',
#                      requires=IS_LENGTH(1048576, 8))),
#             INPUT(_type="submit",
#                   _class="btn btn-primary btn-medium")))
#     paso1 = CENTER(TABLE(
#         form))
#     if form.accepts(request, session):
#         archivos = [
#             request.vars.archivo1,
#             request.vars.archivo2,
#             request.vars.archivo3,
#             request.vars.archivo4,
#         ]
#         archivos_subidos = []

#         path = ('applications/' + str(configuration.get('app.name')) +
#                 '/files/upload/' + hoy_string() + '/')
#         subprocess.run(["mkdir", "-p", path])
#         fecha_h = idtemp_generator(4)
#         for archivo in archivos:
#             nombre = archivo.filename
#             contenido = archivo.file
#             filename = fecha_h + '_' + nombre
#             filepath = path + filename
#             shutil.copyfileobj(contenido, open(filepath, 'wb'))
#             archivos_subidos.append(filename)
#         log('subidos en ' + path + ' : ' + str(archivos_subidos))
#         session.mensaje = {}
#         for archivo in archivos_subidos:
#             session.mensaje[archivo] = subo_cbtes(path + archivo)
#         log(str(session.mensaje))
#         redirect(URL('mensajes'))
#     else:
#         log('acceso ' + str(request.function))
#     return dict(form=paso1)


def subir_datos_afip_paso1():
    session.paso1 = []
    form = FORM(
        H1('Ingrese archivos cabecera zip afip'),
        TABLE(
            TR(INPUT(_name='farchivos', _type='file', _multiple="multiple")),
            INPUT(_type="submit",
                  _class="btn btn-primary btn-medium")))
    paso1 = CENTER(TABLE(
        form))
    if form.accepts(request, session):
        archivos = request.vars.farchivos
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
                archivos_subidos.append(filename)
            log('subidos en ' + path + ' : ' + str(archivos_subidos))
        session.mensaje = {}
        for archivo in archivos_subidos:
            session.mensaje[archivo] = subo_cbtes(path + archivo)
        log(str(session.mensaje))
        redirect(URL('mensajes'))
    else:
        log('acceso ' + str(request.function))
    return dict(form=paso1)


def save_backup():
    nombrecsv = 'bkp_full_' + idtemp_generator(4) + '.csv'
    path = ('applications/' + str(configuration.get('app.name')) +
            '/files/download/backup/' + hoy_string() + '/')
    subprocess.run(["mkdir", "-p", path])
    filepath = path + nombrecsv
    db.export_to_csv_file(open(filepath, 'w', encoding='utf-8', newline=''))
    return response.stream(filepath, request=request,
                           attachment=True, filename=nombrecsv)


def load_backup():
    form = FORM(
        H1('Ingrese archivo bkp_full_*.csv'),
        TABLE(
            TR(INPUT(_name='archivocsv', _type='file',
                     requires=IS_LENGTH(1048576, 8))),
            INPUT(_type="submit",
                  _class="btn btn-primary btn-medium")))
    paso1 = CENTER(TABLE(
        form))
    if form.accepts(request, session):
        archivocsv = request.vars.archivocsv
        path = ('applications/' + str(configuration.get('app.name')) +
                '/files/upload/bkp/' + hoy_string() + '/')
        subprocess.run(["mkdir", "-p", path])
        fecha_h = idtemp_generator(4)
        nombre = archivocsv.filename
        contenido = archivocsv.file
        filename = fecha_h + '_' + nombre
        filepath = path + filename
        shutil.copyfileobj(contenido, open(filepath, 'wb'))
        log('subidos en ' + path + str(filename))
        blank_data()
        session.mensaje = restore_backup(path + filename)
        session.mensaje = path + filename + ' restaurado'
        redirect(URL('mensajes'))
    else:
        log('acceso ' + str(request.function))
    return dict(form=paso1)


def lista_despacho():
    log('acceso ' + str(request.function))
    registros = proceso_detalle_despacho()
    tabla = CENTER(H1('Resultado del analisis de facturas'),
                   list_dict_to_table_sortable(registros))
    form = (tabla)
    return dict(form=form)


@auth.requires_login()
def descarga_csv():
    if session.nombre_archivo:
        log(session.nombre_archivo)
        response.headers['Content-Type'] = 'text/csv'
        attachment = 'attachment;filename=' + str(session.nombre_archivo)
        response.headers['Content-Disposition'] = attachment
        # content = session.lista_consulta
        #
        content = open(str(session.nombre_archivo), "r", encoding='utf8').read()
        # log(content)
        raise HTTP(200, str(content),
                   **{'Content-Type': 'text/csv',
                   'Content-Disposition': attachment + ';'})


# funciones data entry




# _autocomplete="off"
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
    also notice there is http://..../[app]/appadmin/manage/auth to allow
    administrator to manage users
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
