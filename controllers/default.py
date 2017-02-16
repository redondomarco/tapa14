# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

# def index():
#     """
#     example action using the internationalization operator T and flash
#     rendered by views/default/index.html or views/generic.html

#     if you need a simple wiki simply replace the two lines below with:
#     return auth.wiki()
#     """
#     #response.flash = T("Hello World")
#     #return dict(message=T('Welcome to web2py!'))
#     return dict()

@auth.requires_membership('vendedor')
def ingreso():
    #armo tabla de productos
    session.ultimosingresos=SQLFORM.grid(
        db.ingresos,
        fields=(db.ingresos.fecha,db.ingresos.lote,db.ingresos.usuario,db.ingresos.cantidad,db.ingresos.producto),
        orderby=[~db.ingresos.fecha],searchable=False,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    session.productos = []
    session.idsform = []
    tabla1 =[]
    tabla1.append([THEAD(TR(TH('cant'), TH('det'), TH('fis'),TH('net')))])
    for item in db(db.producto.stock_alias==None).select():
        session.productos.append([item.codigo,item.detalle,item.valor,item.stock])
        tabla1.append(TR(
            TD(INPUT(_name='c'+str(item.codigo), _type='number',_min='0',_step='1', _class='cantidad')),
            TD(item.detalle),
            TD(item.stock),
            TD(item.stock-item.reserva)))
            #TD(item.valor, _id='v'+str(item.codigo)),
            #TD(INPUT(_id='s'+str(item.codigo), _type="number",_class='precio', _disabled="disabled"))))
        session.idsform.append(['c'+str(item.codigo),'v'+str(item.codigo),'s'+str(item.codigo)])
    #tabla1.append(TFOOT(TR(TH(''), TH(''), TH(''),
    #    TH('Total',_id='totaltitle'),
    #    TH(INPUT(_id='totalt', _type="number",_class='precio', _disabled="disabled")))))
    #formulario
    #logger.info(str(session.idsform))
    form_ingreso = FORM(
        CENTER(
            H3('Ingreso de producción'),
            TABLE(
                TR(
                    TAG('<label class="tabla-label">Fecha: </label>'),
                    INPUT(_class='date',_name='ingresofecha',_id='fechaingreso'),
                    TAG('<label for="clienteinput">Lote:</label>'),
                    INPUT(_name='ingresolote', _type='number',_min='1',_max='365',_step='1', _class='nrolote')),
            _id='tablaingreso'
            )),
        TABLE( tabla1, _class='t2', _id="suma"),
        CENTER( INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='ingresar',_id='button14')),)
    if form_ingreso.accepts(request, session):
        for item in db(db.producto.detalle).select():
            cant='c'+str(item.codigo)
            if request.vars['ingresofecha']!='':
                ingresofecha=datetime.strptime(request.vars['ingresofecha'], '%d/%m/%Y')
            else:
                ingresofecha=''
            ingresolote=request.vars['ingresolote']
            cantidad=request.vars[cant]
            if cantidad == '' or cantidad == None:
                cantidad=int(0)
            db(db.producto.codigo==item.codigo).update(stock=db(db.producto.codigo==item.codigo).select()[0].stock+int(cantidad))
            if cantidad!=0:
                #logger.info(str(auth.user.email))
                log(str(cantidad)+' '+str(item.codigo)+' desde '+str(request.client)+' fecha '+str(ingresofecha)+' lote '+str(ingresolote))
                producto=db(db.producto.codigo==item.codigo).select().first()['detalle']
                productoid=db(db.producto.codigo==item.codigo).select().first()['id']
                db.ingresos.insert(
                    fecha=datetime.now(),
                    fecha_prod=ingresofecha,
                    lote=ingresolote,
                    vencimiento=fecha_vto(ingresolote),
                    usuario=auth.user.email,
                    cantidad=cantidad,
                    producto=productoid)
        db.commit()
        #logger.info("bien")
        redirect(URL('index'))
        #logger.flash("ingresados")
    else:
        log('acceso')
        #logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    return dict(form_ingreso=form_ingreso, ids_json=json(session.idsform))

#armo tabla de productos para venta y calculadora
session.productos = []
session.idsform = []
tabla1 = [THEAD(TR(TH('cant'), TH('detalle'), TH('stock'), TH('final'),TH('sub')))]
for item in db(db.producto.detalle).select():
    session.productos.append([item.codigo,item.detalle,item.valor,item.stock])
    tabla1.append(TR(
        TD(INPUT(_id='c'+str(item.codigo), _name='c'+str(item.codigo),_type='number',_min='0',_step='1', _class='cantidad')),
        TD(item.detalle),
        TD(item.stock),
        TD(item.valor, _id='v'+str(item.codigo)),
        TD(INPUT(_id='s'+str(item.codigo), _type="number",_class='precio', _disabled="disabled"))))
    session.idsform.append(['c'+str(item.codigo),'v'+str(item.codigo),'s'+str(item.codigo)])
tabla1.append(TFOOT(TR(TH(''), TH(''), TH(''),
    TH('Total',_id='totaltitle'),
    TH(INPUT(_id='totalt', _type="number",_class='precio', _disabled="disabled")))))

@auth.requires_membership('vendedor')
def ventaold():
    clientes=db(db.cliente).select(db.cliente.ALL)
    listas=db(db.listas).select(db.listas.ALL)
    comprobante=db(db.comprobante.nombre=='venta').select().first()['lastid']
    logger.info("tabla1: "+str(tabla1))
    form_venta = FORM(
        CENTER(
            TABLE(
                TR(
                    #TAG('<label class="control-label">Cliente </label>'),
                    TAG('<label for="clienteinput">cliente</label>'),
                    SELECT([" "]+[(p.nombre) for p in clientes], _name='cliente', _type='text', _id="clienteinput",_class="form-control string"),
                    TAG('<label class="control-label">Venta nº </label>'),
                    INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_class="form-control string",_id='nrocomp')),
            _id='tablacliente'
            ),
        ),
        TABLE( tabla1, _class='t2', _id="suma"),
        CENTER( INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='vender',_id='button14')),
        _id='formventa')
    if form_venta.accepts(request, session):
        logger.info('aceptado '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
        cliente=request.vars['cliente']
        if cliente==" ":
            logger.info('cliente vacio '+str(cliente))
            redirect(URL('index'))
        else:
            logger.info('cliente:'+str(cliente))
        ventanumactual=db(db.comprobante.nombre=='venta').select()[0].lastid
        listaid=db(db.cliente.nombre==cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        for item in db(db.producto.detalle).select():
            cant='c'+str(item.codigo)
            #logger.info("cant: "+str(cant)+str(request.vars))
            #logger.info(str(request.vars[cant])+str(type(request.vars[cant])))
            #cantidad=int(str(request.vars[cant]))
            #logger.info('cantTTTTT'+str(type(cantidad))+'|'+str(cantidad)+'|')
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))
            #logger.info("cantidad:"+str(cantidad))
            db(db.producto.codigo==item.codigo).update(stock=db(db.producto.codigo==item.codigo).select()[0].stock-int(cantidad))
            if cantidad!=0:
                valor=float(db(db.producto.codigo==item.codigo).select().first()['valor'])
                producto=db(db.producto.codigo==item.codigo).select().first()['detalle']
                productoid=db(db.producto.codigo==item.codigo).select().first()['id']
                vendedorid=db(db.auth_user.email==auth.user.email).select().first()['id']
                clienteid=db(db.cliente.nombre==cliente).select().first()['id']
                listaid=db(db.cliente.nombre==cliente).select().first()['lista']
                descuento=float(db(db.listas.id==listaid).select().first()['valor'])
                preciou=round(valor*descuento,2)
                total=preciou*int(cantidad)
                logger.info(str(auth.user.email)+' venta #'+str(ventanumactual)+' cant '+str(cantidad)+' '+str(producto)+' pu '+str(preciou)+' total '+str(total)+' a '+str(cliente)+' desde '+str(request.client))
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
        db(db.comprobante.nombre=='venta').update(lastid=db(db.comprobante.nombre=='venta').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    return dict(form_venta=form_venta, ids_json=json(session.idsform), clientes_json=json(clientes), listas_json=json(listas))

@auth.requires_membership('vendedor')
def selec_cliente():
    clientes=db(db.cliente).select(db.cliente.ALL)
    form = FORM(
        CENTER(
            TAG('<label class="control-label">Venta </label>'),BR(),
            TABLE(
                TR(
                    TAG('<label for="clienteinput"> cliente</label>'),
                    SELECT([" "]+[(p.nombre) for p in clientes], _name='cliente', _type='text', _id="clienteinput",_class="form-control string")
                ),
                _id='tablaselec',
            ),
            BR(),INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='continuar',_id='button14'),BR(),
        ),
        _id='formventa')
    if form.accepts(request, session):
        session.cliente=request.vars['cliente']
        logger.info('aceptado '+str(request.function)+' '+str(session.cliente)+' '+str(auth.user.email)+' from '+str(request.cookies))
        redirect(URL('venta'))
    return dict(form=form)


@auth.requires_membership('vendedor')
def venta():
    #clientes=db(db.cliente).select(db.cliente.ALL)
    listas=db(db.listas).select(db.listas.ALL)
    comprobante=db(db.comprobante.nombre=='venta').select().first()['lastid']
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
    tabla3 = []

    tabla2 = []
    #tabla2.append(THEAD(TR(TH(),TH('cliente'), TH('cod.'),TH('sub'))))
    #tabla2.append(THEAD(TR(TH(' '))))
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
        CENTER(
            #TAG('<label class="control-label">Venta </label>'),BR(),
            TABLE(
                TR(
                    TAG('<label class="tabla-label">Venta nº </label>'),
                    INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_id='nrocomp')),
                TR(
                    TAG('<label for="clienteinput">cliente</label>'),
                    INPUT(_value=str(session.cliente), _name='cliente', _disabled="disabled",_type='text', _id="clienteinput")),
            _id='tablacliente'
            )
        ),
        TABLE( tabla2, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='vender',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        productovendido=False
        logger.info('aceptado '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
        ventanumactual=db(db.comprobante.nombre=='venta').select()[0].lastid
        listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        for item in productos_cliente:
            producto=db(db.producto.id==item).select().first()
            cant='c'+str(item.codigo)
            #logger.info("cant: "+str(cant)+str(request.vars))
            #logger.info(str(request.vars[cant])+str(type(request.vars[cant])))
            #cantidad=int(str(request.vars[cant]))
            #logger.info('cantTTTTT'+str(type(cantidad))+'|'+str(cantidad)+'|')
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))
            #logger.info("cantidad:"+str(cantidad))
            
            if cantidad!=0:
                productovendido=True
                #logica descuento stock
                if producto['stock_alias']==None:
                    db(db.producto.codigo==producto['codigo']).update(stock=db(db.producto.codigo==producto['codigo']).select()[0].stock-int(cantidad))
                else:
                    logger.info("---DEBUG---: "+str(producto['stock_alias']))
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
                logger.info(str(auth.user.email)+' venta #'+str(ventanumactual)+' cant '+str(cantidad)+' '+str(detalle)+' pu '+str(preciou)+' total '+str(total)+' a '+str(session.cliente)+' desde '+str(request.client))
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
        #solo subo el numero de venta si no fue todo 0
        if productovendido:
            db(db.comprobante.nombre=='venta').update(lastid=db(db.comprobante.nombre=='venta').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
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
        logger.info('aceptado '+str(request.function)+' '+str(session.cliente)+' '+str(auth.user.email)+' from '+str(request.cookies))
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
    tabla2 = [THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'),TH('sub')))]
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
        CENTER(
            TAG('<label class="control-label">Pedido </label>'),BR(),
            TABLE(
                TR(
                    #TAG('<label class="control-label">Cliente </label>'),
                    TAG('<label for="clienteinput">cliente</label>'),
                    INPUT(_value=str(session.cliente), _name='cliente', _type='text', _id="clienteinput",_class="form-control string"),
                    TAG('<label class="control-label">Pedido nº </label>'),
                    INPUT(_value=str(int(comprobante)).zfill(10),_disabled="disabled",_class="form-control string",_id='nrocomp')),
            _id='tablacliente'
            )
        ),
        TABLE( tabla2, _class='t2', _id="suma"),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='Generar Pedido',_id='button14')),
        _id='formventa')
    if form.accepts(request, session):
        logger.info('aceptado '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
        pedidonumactual=db(db.comprobante.nombre=='pedido').select()[0].lastid
        listaid=db(db.cliente.nombre==session.cliente).select().first()['lista']
        desc_lista=db(db.listas.id==listaid).select().first()['valor']
        for item in productos_cliente:
            producto=db(db.producto.id==item).select().first()
            cant='c'+str(item.codigo)
            #logger.info("cant: "+str(cant)+str(request.vars))
            #logger.info(str(request.vars[cant])+str(type(request.vars[cant])))
            #cantidad=int(str(request.vars[cant]))
            #logger.info('cantTTTTT'+str(type(cantidad))+'|'+str(cantidad)+'|')
            if request.vars[cant] == '':
                cantidad=int(0)
            else:
                cantidad=int(str(request.vars[cant]))
            #logger.info("cantidad:"+str(cantidad))
            
            if cantidad!=0:
                #logica descuento stock
                if producto['stock_alias']==None:
                    db(db.producto.codigo==producto['codigo']).update(stock=db(db.producto.codigo==producto['codigo']).select()[0].stock-int(cantidad))
                else:
                    logger.info("---DEBUG---: "+str(producto['stock_alias']))
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
                logger.info(str(auth.user.email)+' pedido #'+str(pedidonumactual)+' cant '+str(cantidad)+' '+str(detalle)+' pu '+str(preciou)+' total '+str(total)+' a '+str(session.cliente)+' desde '+str(request.client))
                db.pedidos.insert(
                    fecha=datetime.datetime.now(),
                    vendedor=vendedorid,
                    cliente=clienteid,
                    pedidonum=pedidonumactual,
                    cantidad=int(cantidad),
                    producto=productoid,
                    preciou=preciou,
                    terminado=False,
                    total=total
                    )
        db(db.comprobante.nombre=='pedido').update(lastid=db(db.comprobante.nombre=='pedido').select()[0].lastid+1)
        db.commit()
        redirect(URL('index'))
    else:
        logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    return dict(form=form, ids_json=json(idsform), listas_json=json(listas), descuento=descuento, precios_json=json(precios))

@auth.requires_membership('vendedor')
def pedido_pendiente():
    logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(
        db.pedidos,
        fields=(db.pedidos.fecha,db.pedidos.pedidonum,db.pedidos.vendedor,db.pedidos.cliente,db.pedidos.cantidad,db.pedidos.producto,db.pedidos.preciou,db.pedidos.total),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    form = FORM(
        CENTER(
            TABLE(
                TR(
                    TAG('<label class="control-label">Finalizar pedido nº </label>'),
                    INPUT(_class="form-control string",_id='nrocomp')),
            _id='tablacliente'
            )
        ),
        CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium", _value='Vender',_id='button14')),
        _id='formventa')
    return dict(grid=grid, form=form)



@auth.requires_membership('vendedor')
def index2():
    #formulario
    #logger.info(str(session.idsform))
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
        logger.info("bien")
    else:
        logger.info("no tanto")
    return dict(form_venta=form_venta, ids_json=json(session.idsform), clientes_json=json(clientes), listas_json=json(listas))

@auth.requires_membership('vendedor')
def index():
    return dict()

@auth.requires_membership('admin')
def productos():
    logger.info('acceso admin '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(db.producto)
    return locals()

@auth.requires_membership('admin')
def clientes():
    logger.info('acceso admin '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(db.cliente,maxtextlength=25)
    return locals()

@auth.requires_membership('admin')
def listas():
    logger.info('acceso admin '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(db.listas,maxtextlength=25)
    return locals()

@auth.requires_membership('admin')
def productos():
    logger.info('acceso admin '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(db.producto,maxtextlength=25)
    return locals()

@auth.requires_membership('productor')
def consulta_ingreso_stock():
    logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(
        db.ingresos,
        fields=(db.ingresos.fecha,db.ingresos.usuario,db.ingresos.cantidad,db.ingresos.producto),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

@auth.requires_membership('vendedor')
def consulta_venta_stock():
    logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(
        db.ventas,
        fields=(db.ventas.fecha,db.ventas.ventanum,db.ventas.vendedor,db.ventas.cliente,db.ventas.cantidad,db.ventas.producto,db.ventas.preciou,db.ventas.total),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

@auth.requires_membership('vendedor')
def consulta_stock():
    logger.info('acceso '+str(request.function)+' '+str(auth.user.email)+' from '+str(request.cookies))
    grid=SQLFORM.grid(
        db.producto,
        fields=(db.producto.codigo,db.producto.detalle,db.producto.valor,db.producto.stock),
        searchable=True,editable=False,deletable=False,create=False,sortable=True,details=False,maxtextlength=25)
    return locals()

def admin():
    return dict()

def mensajes():
    return dict()

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


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


