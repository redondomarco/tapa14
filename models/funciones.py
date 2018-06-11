#funciones sobre el modelo
def arbol_pedidos():
	pedidos=db(db.pedidos).select(db.pedidos.ALL).as_list()
	auxnum=[]
	fichas=tree()
	for i in pedidos:
		pedidonum=i['pedidonum']
		cantidad=i['cantidad']
		idcliente=i['cliente']
		try:
			fentrega=i['fentrega'].strftime('%d/%m')
		except Exception as e:
			fentrega=''
		cliente=db(db.cliente.id==idcliente).select().first()['nombre']
		idproducto=i['producto']
		producto=db(db.producto.id==idproducto).select().first()['codigo']
		nota=i['nota']
		total=i['total']
		fichas[cliente][pedidonum][producto]=[cantidad,nota,fentrega,total]
	return fichas