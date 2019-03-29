# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import subprocess
from gluon.tools import Expose
# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    from db import *


@auth.requires_membership('vendedor')
def index():
    log('ingreso')
    form = FORM(CENTER(TABLE(
        TR(H4('stock'),
           CENTER(A('ingreso', _class="btn btn-primary",
                  _href=URL('ingreso'))),
           CENTER(A('venta', _class="btn btn-primary",
                  _href=URL('selec_cliente'))),
           ),
        TR(),
        TR(H4('consultas'),
           CENTER(A('ingresos', _class="btn btn-primary",
                  _href=URL('consulta_ingreso_stock'))),
           CENTER(A('ventas', _class="btn btn-primary",
                  _href=URL('consulta_venta_stock'))),
           CENTER(A('stock', _class="btn btn-primary",
                  _href=URL('consulta_stock')))
           ),
        TR(),
        TR(H4('pedidos'),
           CENTER(A('nuevo', _class="btn btn-primary",
                  _href=URL('selec_cliente_pedido'))),
           CENTER(A('pendientes', _class="btn btn-primary",
                  _href=URL('pedido_pendiente')))
           ),
        TR(),
        TR(
            H4('materia prima'),
            CENTER(A('ingreso', _class="btn btn-primary",
                   _href=URL('ingreso_mp'))),
            CENTER(A('baja', _class="btn btn-primary",
                   _href=URL('baja_mp')))
        ),
        _id='tablaindex'
    ),
    )
    )
    return dict(form=form)


@auth.requires_membership('vendedor')
def ingreso():
    # armo tabla de productos
    session.ultimosingresos = SQLFORM.grid(
        db.ingresos,
        fields=(db.ingresos.fecha, db.ingresos.lote,
                db.ingresos.usuario, db.ingresos.cantidad,
                db.ingresos.producto),
        orderby=[~db.ingresos.fecha],
        searchable=False, editable=False, deletable=False, create=False,
        sortable=True, details=False, maxtextlength=25)
    session.productos = []
    session.idsform = []
    tabla1 = []
    tabla1.append([THEAD(TR(TH('cant'), TH('det'), TH('fis'), TH('net')))])
    for item in db(db.producto.stock_alias is None).select():
        session.productos.append([item.codigo,
                                  item.detalle,
                                  item.valor,
                                  item.stock])
        tabla1.append(TR(
            TD(INPUT(_name='c' + str(item.codigo),
                     _type='number', _min='0', _step='1', _class='cantidad')),
            TD(item.detalle),
            TD(item.stock),
            TD(item.stock - item.reserva)))
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
            TABLE(
                TR(
                    TAG('<label class="tabla-label">Fecha: </label>'),
                    INPUT(_class='date', _name='ingresofecha',
                          _id='fechaingreso'),
                    TAG('<label for="clienteinput">Lote:</label>'),
                    INPUT(_name='ingresolote', _type='number', _min='1',
                          _max='365', _step='1', _class='nrolote')),
                _id='tablaingreso'),
            TABLE(tabla1, _class='t2', _id="suma"),
            TABLE(TR(A('Volver', _href=request.env.http_referer,
                  _class='btn btn-default'),
                  INPUT(_type="submit", _class="btn btn-primary btn-medium",
                        _value='ingresar', _id='button14')))))
    if form_ingreso.accepts(request, session):
        for item in db(db.producto.detalle).select():
            cant = 'c' + str(item.codigo)
            if request.vars['ingresofecha'] != '':
                hora = (request.vars['ingresofecha'].replace('/', '-') +
                        ' 12:00:00', '%d-%m-%Y %H:%M:%S')
                ingresofecha = datetime.strptime(hora)
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
            db(selector).update(
                stock=db(selector).select()[0].stock + int(cantidad))
            if cantidad != 0:
                log(str(cantidad) + ' ' + str(item.codigo) + ' desde ' +
                    str(request.client) + ' fecha ' +
                    str(ingresofecha) + ' lote ' + str(ingresolote))
                s_producto = (db.producto.codigo == item.codigo)
#                producto = db(s_producto).select().first()['detalle']
                productoid = db(s_producto).select().first()['id']
                db.ingresos.insert(
                    fecha=datetime.now(),
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
    return dict(form_ingreso=form_ingreso, ids_json=json(session.idsform))


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


@auth.requires_membership('vendedor')
def selec_cliente():
    clientes = db(db.cliente).select(db.cliente.ALL)
    form = FORM(
        CENTER(
            H3('Venta'),
            TABLE(
                TR(TAG('<label for="clienteinput"> cliente</label>'),
                   SELECT([" "]+[(p.nombre) for p in clientes], _name='cliente', _type='text', _id="clienteinput",_class="form-control string"),
                ),
                TR(TAG('<label class="tabla-label">Fecha Entrega: </label>'),
                   SELECT(["Inmediata"]+["Posterior"], _name='entrega', _type='text', _id="clienteinput",_class="form-control string")
                ),
                _id='tablaselec',
            ),
            BR(),INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='continuar',_id='button14'),BR(),
        ),
        _id='formventa')
    if form.accepts(request, session):
        session.cliente=request.vars['cliente']
        session.entrega=request.vars['entrega']
        debug(str(session.cliente))
        if session.cliente!=" ":
            log('aceptado')
            redirect(URL('venta'))
        else:
            redirect(URL('selec_cliente'))
    return dict(form=form)


@auth.requires_membership('vendedor')
def venta():
    listas = db(db.listas).select(db.listas.ALL)
    s_venta = (db.comprobante.nombre == 'venta')
    comprobante = db(s_venta).select().first()['lastid']
    session.ultimasventas = SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha, db.ventas.ventanum, db.ventas.vendedor,
                db.ventas.cliente, db.ventas.cantidad, db.ventas.producto,
                db.ventas.total),
        orderby=[~db.ventas.fecha],
        searchable=False, editable=False, deletable=False, create=False,
        sortable=True, details=False, maxtextlength=25)
#   creo tabla con productos habilitados para el cliente
    session.productos = []
    idsform = []
    precios = []
    productos_cliente=db(db.cliente.nombre==session.cliente).select().first()['productos']
    tipocuenta=db(db.cliente.nombre==session.cliente).select().first()['tipocuenta']
    log(tipocuenta)
    log(session.cliente)
    #if idtipocuenta==None:
    #    session.mensaje='El cliente no tiene tipo de cuenta valida'
    #    redirect(URL('mensajes'))
    listaidcliente=db(db.cliente.nombre==session.cliente).select().first()['lista']
    descuento=db(db.listas.id==listaidcliente).select().first()['valor']
    if productos_cliente==None:
        session.mensaje='El cliente no tiene productos habilitados'
        redirect(URL('mensajes'))
    nro_venta=TR(TAG('<label class="tabla-label">Venta nº </label>'),
                INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_id='nrocomp'))
    nombre_cliente=TR(TAG('<label for="clienteinput">cliente</label>'),
                     INPUT(_value=str(session.cliente), _name='cliente', _disabled="disabled",_type='text', _id="clienteinput"))
    tipo_cuenta=TR(TAG('<label for="tipocuenta">cuenta</label>'),
                   INPUT(_value=str(tipo_cta), _name='tipocuenta', _disabled="disabled",_type='text', _id="tipocuenta"))
    if tipocuenta=='|efectivo|':
        tablacliente=TABLE(
                nro_venta,
                nombre_cliente,
                tipo_cuenta,
                _id='tablacliente'
                )
    elif tipocuenta=='|cta cte|':
        saldo_cliente=db(db.cliente.nombre==session.cliente).select().first()['saldo']
        if saldo_cliente<0:
            tagid='saldonegativo'
        else:
            tagid='tipocuenta'
        saldo=TR(TAG('<label for="tipocuenta">saldo</label>'),
                 INPUT(_value=str(saldo_cliente), _disabled="disabled",_type="number",_class=tagid))
        if session.entrega=='Inmediata':
            fecha_entrega=""
        elif session.entrega=="Posterior":
            fecha_entrega=TR(TAG('<label class="tabla-label">Entrega: </label>'),
                             INPUT(_class='date',_name='fechaentrega',_id='fechaingreso'))
        tablacliente=TABLE(
                nro_venta,
                nombre_cliente,
                tipo_cuenta,
                saldo,
                fecha_entrega,
                _id='tablacliente'
                )
    else:
        session.mensaje='El cliente no tiene tipo de cuenta valida'
        redirect(URL('mensajes'))
    #genero tabla para form
    tabla2 = []
    tabla2.append(THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'),TH('sub'))))
    for item in productos_cliente:
        producto=db(db.producto.id==item).select().first()
        session.productos.append([producto['codigo'],producto['detalle'],producto['valor']])
        tabla2.append(TR(
            TD(INPUT(_id='c'+str(producto['codigo']), _name='c'+str(producto['codigo']),_type='number',_min='0',_step='1', _class='cantidad')),
            TD(producto['detalle']),
            TD(producto['codigo'], _id='v'+str(producto['codigo'])),
            TD(INPUT(_id='s'+str(producto['codigo']), _type="number",_class='precio', _disabled="disabled"))))
        idsform.append(['c'+str(producto['codigo']),'v'+str(producto['codigo']),'s'+str(producto['codigo'])])
        precios.append(producto['valor'])
    tabla2.append(TFOOT(TR(
        TH(''), TH(''), TH('Total',_id='totaltitle'),TH(INPUT(_id='totalt', _type="number",_class='precio', _disabled="disabled")))))
    form = FORM(
        DIV(
        CENTER(tablacliente),
        TABLE( tabla2, _class='t2', _id="suma"),_id='capture'),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='vender',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        productovendido=False
        log('aceptado')
        ventanumactual=db(db.comprobante.nombre=='venta').select()[0].lastid
        listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        for item in productos_cliente:
            producto=db(db.producto.id==item).select().first()
            cant='c'+str(item.codigo)
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))
            if cantidad!=0:
                productovendido=True
                #logica descuento stock
                if producto['stock_alias']==None:
                    db(db.producto.codigo==producto['codigo']).update(stock=db(db.producto.codigo==producto['codigo']).select()[0].stock-int(cantidad))
                else:
                    stockprod=db(db.producto.id==producto['stock_alias']).select().first()
                    db(db.producto.codigo==stockprod['codigo']).update(stock=db(db.producto.codigo==stockprod['codigo']).select()[0].stock-int(cantidad))
                valor=float(producto['valor'])
                detalle=producto['detalle']
                productoid=producto['id']
                vendedorid=db(db.auth_user.email==auth.user.email).select().first()['id']
                clienteid=db(db.cliente.nombre==session.cliente).select().first()['id']
                listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
                preciou=round(valor*descuento,2)
                total=preciou*int(cantidad)
                log('venta #'+str(ventanumactual)+' cant '+str(cantidad)+' '+str(detalle)+' pu '+str(preciou)+' total '+str(total)+' a '+str(session.cliente))
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
        #solo subo el numero de venta si no fue todo 0
        if productovendido:
            db(db.comprobante.nombre=='venta').update(lastid=db(db.comprobante.nombre=='venta').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        log(str(session.cliente)+' ingreso')
    return dict(form=form, ids_json=json(idsform), listas_json=json(listas), descuento=descuento, precios_json=json(precios))

def selec_cliente_pedido():
    clientes=db(db.cliente).select(db.cliente.ALL)
    form = FORM(
        CENTER(
            TAG('<label class="control-label">Pedido </label>'),BR(),
            TABLE(
                TR(
                    TAG('<label for="clienteinput"> cliente</label>'),
                    SELECT([" "]+[(p.nombre) for p in clientes], _name='cliente', _type='text', _id="clienteinput",_class="form-control string")
                ),
                _id='tablacliente',
            ),
            BR(),INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='continuar',_id='button14'),BR(),
        ),
        _id='formventa')
    if form.accepts(request, session):
        session.cliente=request.vars['cliente']
        log('seleccionado '+str(session.cliente))
        redirect(URL('pedido'))
    return dict(form=form)


@auth.requires_membership('vendedor')
def pedido():
    #clientes=db(db.cliente).select(db.cliente.ALL)
    listas=db(db.listas).select(db.listas.ALL)
    comprobante=db(db.comprobante.nombre=='pedido').select().first()['lastid']
    #creo tabla con productos habilitados para el cliente
    session.productos = []
    idsform = []
    precios = []
    productos_cliente=db(db.cliente.nombre==session.cliente).select().first()['productos']
    listaidcliente=db(db.cliente.nombre==session.cliente).select().first()['lista']
    descuento=db(db.listas.id==listaidcliente).select().first()['valor']
    if productos_cliente==None:
        session.mensaje='El cliente no tiene productos habilitados'
        redirect(URL('mensajes'))
    #genero tabla para form
    tabla2 = [THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'),TH('dto'),TH('sub')))]
    for item in productos_cliente:
        producto=db(db.producto.id==item).select().first()
        if producto==None:
            session.mensaje='Revisar productos habilitados'
            redirect(URL('mensajes'))
        session.productos.append([producto['codigo'],producto['detalle'],producto['valor']])
        idcant='c'+str(producto['codigo'])
        idvalor='v'+str(producto['codigo'])
        iddto='d'+str(producto['codigo'])
        idsubt='s'+str(producto['codigo'])
        tabla2.append(TR(
            TD(INPUT(_id=idcant, _name=idcant,_type='number',_min='0',_step='1', _class='cantidad')),
            TD(producto['detalle']),
            TD(producto['codigo'], _id=idvalor),
            TD(INPUT(_id=iddto, _name=iddto,_type='number',_min='0',_max='100',_step='1', _class='cantidad')),
            TD(INPUT(_id=idsubt, _type="number",_class='precio', _disabled="disabled"))))
        idsform.append([idcant,idvalor,iddto,idsubt])
        precios.append(producto['valor'])
    tabla2.append(TFOOT(TR(
        TH(''), TH(''),TH(''), TH('Total',_id='totaltitle'),TH(INPUT(_id='totalt', _type="number",_class='precio', _disabled="disabled")))))
    form = FORM(
        CENTER(
            TAG('<label class="control-label">Pedido </label>'),BR(),
            TABLE(
                TR(
                    #TAG('<label class="control-label">Cliente </label>'),
                    TAG('<label for="clienteinput">cliente</label>'),
                    INPUT(_value=str(session.cliente), _name='cliente', _type='text',_disabled="disabled", _id="clienteinput",_class="form-control string"),
                    TAG('<label class="control-label">Pedido nº </label>'),
                    INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_class="form-control string",_id='nrocomp')),
                TR(
                    TAG('<label for="notainput">nota</label>'),
                    INPUT(_name='nota',  _type='text',_id="notainput",_class="form-control string"),
                    TAG('<label for="fechaent">Fecha entrega</label>'),
                    INPUT(_name='entrega',  _type='date',_id="fechaent",_class="form-control string")),
            _id='tablacliente'
            )
        ),
        TABLE( tabla2, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='Generar Pedido',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        log('aceptado')
        pedidonumactual=db(db.comprobante.nombre=='pedido').select()[0].lastid
        listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        nota=request.vars.nota
        log(str(request.vars.entrega))
        if request.vars.entrega!="":
            fentrega=datetime.strptime(request.vars.entrega.replace('/','-')+' 12:00:00', '%Y-%m-%d %H:%M:%S')
        else:
            fentrega=request.vars.entrega
        #fentrega=request.vars.entrega
        #log(str(fentrega)+' '+str(type(fentrega)))
        for item in productos_cliente:
            producto=db(db.producto.id==item).select().first()
            cant='c'+str(item.codigo)
            desc='d'+str(item.codigo)
            #cantidad=int(str(request.vars[cant]))
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))

            if cantidad!=0:
                #logica descuento stock
                if producto['stock_alias']==None:
                    db(db.producto.codigo==producto['codigo']).update(stock=db(db.producto.codigo==producto['codigo']).select()[0].stock-int(cantidad))
                else:
                    stockprod=db(db.producto.id==producto['stock_alias']).select().first()
                    db(db.producto.codigo==stockprod['codigo']).update(stock=db(db.producto.codigo==stockprod['codigo']).select()[0].stock-int(cantidad))
                valor=float(producto['valor'])
                detalle=producto['detalle']
                productoid=producto['id']
                vendedorid=db(db.auth_user.email==auth.user.email).select().first()['id']
                clienteid=db(db.cliente.nombre==session.cliente).select().first()['id']
                listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
                preciou=round(valor*descuento,2)
                total=preciou*int(cantidad)
                log('pedido #'+str(pedidonumactual)+' cant '+str(cantidad)+' '+str(detalle)+' pu '+str(preciou)+' total '+str(total)+' a '+str(session.cliente))
                db.pedidos.insert(
                    fecha=datetime.now(),
                    fentrega=fentrega,
                    pedidonum=pedidonumactual,
                    vendedor=vendedorid,
                    cliente=clienteid,
                    nota=str(nota),
                    cantidad=int(cantidad),
                    producto=productoid,
                    preciou=preciou,
                    total=total
                    )

        db(db.comprobante.nombre=='pedido').update(lastid=db(db.comprobante.nombre=='pedido').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        log('ingreso')
    return dict(form=form, ids_json=json(idsform), listas_json=json(listas), descuento=descuento, precios_json=json(precios))

@auth.requires_membership('vendedor')
def pedido_pendiente():
    pedidos=arbol_pedidos()
    #genero elementos grilla
    conjunto_fichas=[]
    for cliente in pedidos.keys():
        total=0
        productosficha=[]
        #setpedidos=[]
        for pedido in pedidos[cliente].keys():
            #setpedidos.append(pedido)
            nota=db(db.pedidos.pedidonum==int(pedido)).select(db.pedidos.nota).first()['nota']
            productosficha.append(H4('Pedido n°'+str(pedido),_id='itemficha'))
            productosficha.append(DIV(nota))
            for producto in pedidos[cliente][pedido].keys():
                cantidad=pedidos[cliente][pedido][producto][0]
                #nota=pedidos[cliente][pedido][producto][1]
                fentrega=pedidos[cliente][pedido][producto][2]
                total=int(total)+int(pedidos[cliente][pedido][producto][3])
                #total='nada'
                item=str(cantidad)+' '+str(producto)+' '+str(fentrega)
                productosficha.append(TR(
                    TD(item,_id='itemficha')))
            productosficha.append(TR(
                TD(DIV(A('Generar NV',_href=URL('nota_de_venta', vars=dict(pedido=pedido)),_class='btn btn-default'))),
                TD(DIV(A('Ingresar Pago',_href=URL('ingreso_pago', vars=dict(pedido=pedido)),_class='btn btn-default')))
                ))
            productosficha.append(TR(BR()))
            unaficha=DIV(CENTER(
                H3(cliente),
                TABLE(productosficha)),
                BR(),
                DIV('TOTAL $ '+str(total),_id='aderecha'),
                _class="grid__item js-item")
        conjunto_fichas.append(unaficha)
    #armo div grilla
    grilla=DIV(conjunto_fichas,_class="grid")
    #auxnum.append(pedidonum)
    #pedidonum=set(auxnum)


    grid=SQLFORM.grid(
        db.pedidos,
        fields=(
            db.pedidos.fecha,db.pedidos.pedidonum,db.pedidos.vendedor,
            db.pedidos.cliente,db.pedidos.cantidad,db.pedidos.producto,
            db.pedidos.preciou,db.pedidos.total),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    form = FORM(
        CENTER(
            TABLE(
                TR(
                    TAG('<label class="control-label">Finalizar pedido nº </label>'),
                    INPUT(_name="pedidonum",_class="form-control string",_id='nrocomp')),
            _id='tablacliente'
            )
        ),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='Vender',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        session.pedido=request.vars.pedidonum
        redirect(URL('finaliza_pedido'))
    return dict(grid=grid, form=form, grilla=grilla)

def nota_de_venta():
    session.pedidoa=request.vars['pedido']
    
    



@auth.requires_membership('vendedor')
def finaliza_pedido():
    pedidos=db(db.pedidos.pedidonum==session.pedido).select().as_dict().values()
    session.clienteid=pedidos[0]['cliente']
    session.cliente=db(db.cliente.id==session.clienteid).select().first()['nombre']
    listas=db(db.listas).select(db.listas.ALL)
    comprobante=db(db.comprobante.nombre=='venta').select().first()['lastid']
    session.ultimasventas=SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha,db.ventas.ventanum,db.ventas.vendedor,db.ventas.cliente,db.ventas.cantidad,db.ventas.producto,db.ventas.total),
        orderby=[~db.ventas.fecha],searchable=False,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    #creo tabla con productos habilitados para el cliente
    session.productos = []
    idsform = []
    precios = []
    productos_cliente=db(db.cliente.nombre==session.cliente).select().first()['productos']
    idtipocuenta=db(db.cliente.nombre==session.cliente).select().first()['tipocuenta']
    if idtipocuenta!=None:
        tipocuenta=db(db.tipo_cta.id==idtipocuenta).select().first()['tipo']
    else:
        session.mensaje='El cliente no tiene tipo de cuenta valida'
        redirect(URL('mensajes'))
    listaidcliente=db(db.cliente.nombre==session.cliente).select().first()['lista']
    descuento=db(db.listas.id==listaidcliente).select().first()['valor']
    if productos_cliente==None:
        session.mensaje='El cliente no tiene productos habilitados'
        redirect(URL('mensajes'))
    nro_venta=TR(TAG('<label class="tabla-label">Venta nº </label>'),
                INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_id='nrocomp'))
    nombre_cliente=TR(TAG('<label for="clienteinput">cliente</label>'),
                     INPUT(_value=str(session.cliente), _name='cliente', _disabled="disabled",_type='text', _id="clienteinput"))
    tipo_cuenta=TR(TAG('<label for="tipocuenta">cuenta</label>'),
                   INPUT(_value=str(tipocuenta), _name='tipocuenta', _disabled="disabled",_type='text', _id="tipocuenta"))
    if tipocuenta=='efectivo':
        tablacliente=TABLE(
                nro_venta,
                nombre_cliente,
                tipo_cuenta,
                _id='tablacliente'
                )
    elif tipocuenta=='cta cte':
        saldo_cliente=db(db.cliente.nombre==session.cliente).select().first()['saldo']
        if saldo_cliente<0:
            tagid='saldonegativo'
        else:
            tagid='tipocuenta'
        saldo=TR(TAG('<label for="tipocuenta">saldo</label>'),
                 INPUT(_value=str(saldo_cliente), _disabled="disabled",_type="number",_class=tagid))
        if session.entrega=='Inmediata':
            fechaentrega=""
        elif session.entrega=="Posterior":
            fecha_entrega=TR(TAG('<label class="tabla-label">Entrega: </label>'),
                             INPUT(_class='date',_name='fechaentrega',_id='fechaingreso'))
        tablacliente=TABLE(
                nro_venta,
                nombre_cliente,
                tipo_cuenta,
                saldo,
                _id='tablacliente'
                )
    else:
        session.mensaje='El cliente no tiene tipo de cuenta valida'
        redirect(URL('mensajes'))
    #genero tabla para form
    tabla2 = []
    tabla2.append(THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'),TH('sub'))))
    for item in productos_cliente:
        #
        #for uno in pedidos:
        #    if 
        #
        producto=db(db.producto.id==item).select().first()
        session.productos.append([producto['codigo'],producto['detalle'],producto['valor']])
        tabla2.append(TR(
            TD(INPUT(_id='c'+str(producto['codigo']), _name='c'+str(producto['codigo']),_type='number',_min='0',_step='1', _class='cantidad')),
            TD(producto['detalle']),
            TD(producto['codigo'], _id='v'+str(producto['codigo'])),
            TD(INPUT(_id='s'+str(producto['codigo']), _type="number",_class='precio', _disabled="disabled"))))
        idsform.append(['c'+str(producto['codigo']),'v'+str(producto['codigo']),'s'+str(producto['codigo'])])
        precios.append(producto['valor'])
    tabla2.append(TFOOT(TR(
        TH(''), TH(''), TH('Total',_id='totaltitle'),TH(INPUT(_id='totalt', _type="number",_class='precio', _disabled="disabled")))))
    form = FORM(
        CENTER(tablacliente),
        TABLE( tabla2, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='vender',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        productovendido=False
        log('aceptado')
        ventanumactual=db(db.comprobante.nombre=='venta').select()[0].lastid
        listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        for item in productos_cliente:
            producto=db(db.producto.id==item).select().first()
            cant='c'+str(item.codigo)
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))
            if cantidad!=0:
                productovendido=True
                #logica descuento stock
                if producto['stock_alias']==None:
                    db(db.producto.codigo==producto['codigo']).update(stock=db(db.producto.codigo==producto['codigo']).select()[0].stock-int(cantidad))
                else:
                    stockprod=db(db.producto.id==producto['stock_alias']).select().first()
                    db(db.producto.codigo==stockprod['codigo']).update(stock=db(db.producto.codigo==stockprod['codigo']).select()[0].stock-int(cantidad))
                valor=float(producto['valor'])
                detalle=producto['detalle']
                productoid=producto['id']
                vendedorid=db(db.auth_user.email==auth.user.email).select().first()['id']
                clienteid=db(db.cliente.nombre==session.cliente).select().first()['id']
                listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
                preciou=round(valor*descuento,2)
                total=preciou*int(cantidad)
                log('venta #'+str(ventanumactual)+' cant '+str(cantidad)+' '+str(detalle)+' pu '+str(preciou)+' total '+str(total)+' a '+str(session.cliente))
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
        #solo subo el numero de venta si no fue todo 0
        if productovendido:
            db(db.comprobante.nombre=='venta').update(lastid=db(db.comprobante.nombre=='venta').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        log(str(session.cliente)+' ingreso')
    return dict(form=form, ids_json=json(idsform), listas_json=json(listas), descuento=descuento, precios_json=json(precios))


#@auth.requires_membership('vendedor')
def index2():
    #formulario
    clientes=db(db.cliente).select(db.cliente.ALL)
    listas=db(db.listas).select(db.listas.ALL)
    form_venta = FORM(
        CENTER(
            LABEL('Cliente', _id='labelcliente'),
            SELECT([(p.nombre) for p in clientes], _name='cliente', _type='text', _id="clienteinput"),
            TAG('<span class="label label-success">Calculadora</span>')
            ),
        #SELECT([(p.nombre) for p in result], _id='selector', _name="sistema"),
        TABLE( tabla1, _class='t2', _id="suma"), _id='formventa')
    if form_venta.accepts(request, session):
        log('bien')
    else:
        log('no tanto')
    return dict(form_venta=form_venta, ids_json=json(session.idsform), clientes_json=json(clientes), listas_json=json(listas))

#@auth.requires_membership('admin')
#def productos():
#    log('acceso admin')
#    grid=SQLFORM.grid(db.producto)
#    return locals()

@auth.requires_membership('admin')
def clientes():
    log('acceso admin')
    grid=SQLFORM.grid(
        db.cliente,
        maxtextlength=25,
        fields=(db.cliente.nombre,db.cliente.lista,db.cliente.saldo,db.cliente.tipocuenta)
        )
    return locals()

@auth.requires_membership('admin')
def listas():
    log('acceso admin')
    grid=SQLFORM.grid(db.listas,maxtextlength=25)
    return locals()

@auth.requires_membership('admin')
def productos():
    log('acceso admin')
    grid=SQLFORM.grid(db.producto,maxtextlength=25)
    return locals()

@auth.requires_membership('productor')
def consulta_ingreso_stock():
    log('ingreso')
    grid=SQLFORM.grid(
        db.ingresos,
        fields=(db.ingresos.fecha,db.ingresos.usuario,db.ingresos.cantidad,db.ingresos.producto),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

@auth.requires_membership('vendedor')
def consulta_venta_stock():
    log('ingreso')
    grid=SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha,db.ventas.ventanum,db.ventas.vendedor,db.ventas.cliente,db.ventas.cantidad,db.ventas.producto,db.ventas.preciou,db.ventas.total),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

@auth.requires_membership('vendedor')
def consulta_stock():
    log('ingreso')
    grid=SQLFORM.grid(
        db.producto,
        fields=(db.producto.codigo,db.producto.detalle,db.producto.valor,db.producto.stock),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

def test_nv():
    pdfexample=test_genera_nv()
    #mostrar=Expose('/home/marco/web2py/'+pdfexample)
    files=CENTER(
        DIV(A('test_nv',_class="btn btn-primary", _href=URL('test_nv'))),
        DIV(IFRAME(_src='http://127.0.0.1:8000/dev/default/archivo/test/nv/nv_30.pdf',_width="630px",_height='891'))
    )
    return dict(files=files)



def admin():
    log('ingreso')
    form=CENTER(
        H3('Administrar'),
        TABLE(
        TR(
            H4('ABM'),
            A('productos',_class="btn btn-primary", _href=URL('productos')),
            A('clientes',_class="btn btn-primary", _href=URL('clientes')),
            A('listas',_class="btn btn-primary", _href=URL('listas'))
        ),
        TR(),
        TR(
            H4('anula'),
            A('ingreso',_class="btn btn-primary", _href=URL('anula_ingreso')),
            A('venta',_class="btn btn-primary", _href=URL('anula_venta')),
            A('pedido',_class="btn btn-primary", _href=URL('anula_pedido'))
        ),
        TR(
            A('test_nv',_class="btn btn-primary", _href=URL('test_nv'))
            ),
        TR(),
        _id='tablaindex'
    )
)
    return dict(form=form)


@auth.requires_login()
@auth.requires_membership('vendedor')
def archivo():
    expose = ('applications/' + str(configuration.get('app.name')) +
              '/files')

    subprocess.run(["mkdir", "-p", expose])
    return dict(files=Expose(expose, extensions=['.csv', '.pdf']))


def mensajes():
    log('muestro mensaje: ' + str(session.mensaje))
    return dict()


def capture_update():
    log(request.vars.data)
#    return db().insert(data = request.vars.data)


# ---- API (example) -----


@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})

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


def subir_datos_afip_paso1():
    session.paso1 = []
    form = FORM(
        H1('Ingrese zip afip')
        TAG('<span class="label label-success">archivo</span>'),
        INPUT(_name='csvfile', _type='file', requires=IS_LENGTH(1048576, 8)),
        INPUT(_type="submit", _class="btn btn-primary btn-medium"))
    paso1=CENTER(TABLE(
        H1('Carga de lista dni'),
        TAG('Los dni en el archivo deben estar separado por salto de linea, por ejemplo:'),
        PRE('12345678\n23456789', _id='prestyle'),
        form))
    if form.accepts(request, session):
        tablacsv =  csv.reader(request.vars.csvfile.file.read().splitlines())
        for line in tablacsv:
            session.paso1.append(line)
        log('cargado: '+str(session.paso1))
        redirect(URL('carga_lista_dni_paso2'))
    else:
        log('acceso '+str(request.function))
    return dict(form=paso1)




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
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
