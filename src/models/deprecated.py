# @auth.requires_membership('vendedor')
# def selec_cliente():
#     log('acceso')
#     clientes = db(db.cliente).select(db.cliente.ALL)
#     form = FORM(
#         CENTER(
#             H3('Venta'),
#             TABLE(
#                 TR(TAG('<label for="clienteinput"> cliente</label>'),
#                    SELECT([" "] + [(p.nombre) for p in clientes],
#                           _name='cliente', _type='text', _id="clienteinput",
#                           _class="form-control string"),
#                    ),
#                 TR(TAG('<label class="tabla-label">Fecha Entrega: </label>'),
#                    SELECT(["Inmediata"] + ["Posterior"], _name='entrega',
#                           _type='text', _id="clienteinput",
#                           _class="form-control string")
#                    ),
#                 _id='tablaselec',
#             ),
#             INPUT(_type="submit", _class="btn btn-primary btn-medium",
#                   _value='continuar', _id='button14'),
#         ),
#         _id='formventa')
#     if form.accepts(request, session):
#         session.cliente = request.vars['cliente']
#         session.entrega = request.vars['entrega']
#         debug(str(session.cliente))
#         if session.cliente != " ":
#             log('aceptado')
#             redirect(URL('venta'))
#         else:
#             redirect(URL('selec_cliente'))
#     return dict(form=form)


# @auth.requires_membership('vendedor')
# def venta():
#     listas = db(db.listas).select(db.listas.ALL)
#     s_venta = (db.comprobante.nombre == 'venta')
#     comprobante = db(s_venta).select().first()['lastid']
#     session.ultimasventas = SQLFORM.grid(
#         db.ventas,
#         fields=(db.ventas.fecha, db.ventas.ventanum, db.ventas.vendedor,
#                 db.ventas.cliente, db.ventas.cantidad, db.ventas.producto,
#                 db.ventas.total),
#         orderby=[~db.ventas.fecha],
#         searchable=False, editable=False, deletable=False, create=False,
#         sortable=True, details=False, maxtextlength=25)
# #   creo tabla con productos habilitados para el cliente
#     session.productos = []
#     idsform = []
#     precios = []
#     selector = (db.cliente.nombre == session.cliente)
#     productos_cliente = db(selector).select().first()['productos']
#     tipocuenta = db(selector).select().first()['tipocuenta']
#     log(tipocuenta)
#     log(session.cliente)
#     # if idtipocuenta==None:
#     #    session.mensaje='El cliente no tiene tipo de cuenta valida'
#     #    redirect(URL('mensajes'))
#     listaidcliente = db(selector).select().first()['lista']
#     descuento = db(db.listas.id == listaidcliente).select().first()['valor']
#     if productos_cliente is None:
#         session.mensaje = 'El cliente no tiene productos habilitados'
#         redirect(URL('mensajes'))
#     nro_venta = TR(TAG('<label class="tabla-label">Venta nº </label>'),
#                    INPUT(_value=str(int(comprobante)).zfill(10),
#                          _disabled="disabled", _id='nrocomp'))
#     nombre_cliente = TR(TAG('<label for="clienteinput">cliente</label>'),
#                         INPUT(_value=str(session.cliente), _name='cliente',
#                               _disabled="disabled", _type='text',
#                               _id="clienteinput"))
#     tipo_cuenta = TR(TAG('<label for="tipocuenta">cuenta</label>'),
#                      INPUT(_value=str(tipo_cta), _name='tipocuenta',
#                            _disabled="disabled", _type='text',
#                            _id="tipocuenta"))
#     if tipocuenta == '|efectivo|':
#         tablacliente = TABLE(nro_venta,
#                              nombre_cliente,
#                              tipo_cuenta,
#                              _id='tablacliente'
#                              )
#     elif tipocuenta == '|cta cte|':
#         saldo_cliente = db(selector).select().first()['saldo']
#         if saldo_cliente < 0:
#             tagid = 'saldonegativo'
#         else:
#             tagid = 'tipocuenta'
#         saldo = TR(TAG('<label for="tipocuenta">saldo</label>'),
#                    INPUT(_value=str(saldo_cliente), _disabled="disabled",
#                          _type="number", _class=tagid))
#         if session.entrega == 'Inmediata':
#             fecha_entrega = ""
#         elif session.entrega == "Posterior":
#             fecha_entrega = TR(TAG('<label class="tabla-label">' +
#                                    'Entrega: </label>'),
#                                INPUT(_class='date', _name='fechaentrega',
#                                      _id='fechaingreso'))
#         tablacliente = TABLE(nro_venta,
#                              nombre_cliente,
#                              tipo_cuenta,
#                              saldo,
#                              fecha_entrega,
#                              _id='tablacliente'
#                              )
#     else:
#         session.mensaje = 'El cliente no tiene tipo de cuenta valida'
#         redirect(URL('mensajes'))
#     # genero tabla para form
#     tabla2 = []
#     tabla2.append(THEAD(TR(TH('cant'), TH('detalle'), TH('cod.'), TH('sub'))))
#     for item in productos_cliente:
#         producto = db(db.producto.id == item).select().first()
#         session.productos.append([producto['codigo'],
#                                   producto['detalle'],
#                                   producto['valor']])
#         tabla2.append(TR(
#             TD(INPUT(_id='c' + str(producto['codigo']),
#                      _name='c' + str(producto['codigo']),
#                      _type='number', _min='0', _step='1', _class='cantidad')),
#             TD(producto['detalle']),
#             TD(producto['codigo'], _id='v' + str(producto['codigo'])),
#             TD(INPUT(_id='s' + str(producto['codigo']), _type="number",
#                      _class='precio', _disabled="disabled"))))
#         idsform.append(['c' + str(producto['codigo']),
#                         'v' + str(producto['codigo']),
#                         's' + str(producto['codigo'])
#                         ])
#         precios.append(producto['valor'])
#     tabla2.append(TFOOT(TR(
#         TH(''), TH(''), TH('Total', _id='totaltitle'),
#         TH(INPUT(_id='totalt', _type="number", _class='precio',
#                  _disabled="disabled")))))
#     form = FORM(DIV(
#         CENTER(tablacliente),
#         TABLE(tabla2, _class='t2', _id="suma"), _id='capture'),
#         CENTER(INPUT(_type="submit", _class="btn btn-primary btn-medium",
#                      _value='vender', _id='button14')),
#         _id='formventa')
#     if form.accepts(request, session):
#         productovendido = False
#         log('aceptado')
#         sel_cbte = (db.comprobante.nombre == 'venta')
#         ventanumactual = db(sel_cbte).select()[0].lastid
#         sel_cliente = (db.cliente.nombre == session.cliente)
#         listaid = db(sel_cliente).select().first()['lista']
#         # desc_lista = db(db.listas.id == listaid).select().first()['valor']
#         for item in productos_cliente:
#             producto = db(db.producto.id == item).select().first()
#             cant = 'c' + str(item.codigo)
#             if request.vars[cant] == '':
#                 cantidad = int(0)
#             else:
#                 cantidad = int(str(request.vars[cant]))
#             if cantidad != 0:
#                 productovendido = True
#                 # logica descuento stock
#                 if producto['stock_alias'] is None:
#                     sel_prod = (db.producto.codigo == producto['codigo'])
#                     db(sel_prod).update(
#                         stock=db(sel_prod).select()[0].stock - int(cantidad))
#                 else:
#                     sel_id = (db.producto.id == producto['stock_alias'])
#                     stockprod = db(sel_id).select().first()
#                     sel_cod = (db.producto.codigo == stockprod['codigo'])
#                     db(sel_cod).update(
#                         stock=db(sel_cod).select()[0].stock - int(cantidad))
#                 valor = float(producto['valor'])
#                 detalle = producto['detalle']
#                 productoid = producto['id']
#                 sel_email = (db.auth_user.email == auth.user.email)
#                 vendedorid = db(sel_email).select().first()['id']
#                 sel_cli_nom = (db.cliente.nombre == session.cliente)
#                 clienteid = db(sel_cli_nom).select().first()['id']
#                 # listaid = db(sel_cli_nom).select().first()['lista']
#                 preciou = round(valor * descuento, 2)
#                 total = preciou * int(cantidad)
#                 log('venta #' + str(ventanumactual) + ' cant ' +
#                     str(cantidad) + ' ' + str(detalle) + ' pu ' +
#                     str(preciou) + ' total ' + str(total) + ' a ' +
#                     str(session.cliente))
#                 db.ventas.insert(
#                     fecha=datetime.now(),
#                     vendedor=vendedorid,
#                     cliente=clienteid,
#                     ventanum=ventanumactual,
#                     cantidad=int(cantidad),
#                     producto=productoid,
#                     preciou=preciou,
#                     total=total
#                 )
#         # solo subo el numero de venta si no fue todo 0
#         if productovendido:
#             sel_cbte = (db.comprobante.nombre == 'venta')
#             db(sel_cbte).update(
#                 lastid=db(sel_cbte).select()[0].lastid + 1)
#         db.commit()
#         redirect(URL('index'))
#     else:
#         log('ingreso')
#     return dict(form=form, ids_json=json(idsform), listas_json=json(listas),
#                 descuento=descuento, precios_json=json(precios))