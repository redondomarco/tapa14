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

#devuelve lista de pedidos pendientes
def lista_pedidos():
	pedidos=db(db.pedidos).select(db.pedidos.ALL).as_list()
	lista=[]
	for i in pedidos:
		lista.append(int(i['pedidonum']))
	return list(set(lista))


def obtengo_pedido(pedidonum):
	pedido=db(db.pedidos.pedidonum==pedidonum).select(db.pedidos.ALL).as_list()
	cliente_id=pedido[0]['cliente']
	fentrega=pedido[0]['fentrega']
	nota=pedido[0]['nota']
	items=[]
	for i in pedido:
		producto=db(db.producto.id==i['producto']).select().first()['codigo']
		item=[(int(i['cantidad']),producto,i['preciou'])]
		items.append(item)
	return [cliente_id,fentrega,nota,items]

def elimino_pedido(pedidonum):
    #muevo el pedido a tabla pedidos eliminados
    pedido=db(db.pedidos.pedidonum==pedidonum).select(db.pedidos.ALL).as_list()
    for i in pedido:
        db.pedidos_hist.insert(
            fecha=i['fecha'],
            fentrega=i['fentrega'],
            pedidonum=i['pedidonum'],
            vendedor=i['vendedor'],
            cliente=i['cliente'],
            nota=i['nota'],
            cantidad=i['cantidad'],
            producto=i['producto'],
            preciou=i['preciou'],
            total=i['total']
            )
    db(db.pedidos.pedidonum==pedidonum).delete()
    db.commit()
    log('eliminado pedido:'+str(pedidonum))

def obtengo_cliente(clienteid):
	return db(db.cliente.id==clienteid).select(db.cliente.ALL).as_dict()[clienteid]


#from sets import Set
#def quito_ce(palabra):
#    caracteres_permitidos='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    allowed_chars = Set(caracteres_permitidos)
#    if palabra==None:
#    	return 'error'
#    resultado=''
#    for i in palabra:
#        if i in allowed_chars:
#            resultado=resultado+i
#    return resultado

    #if Set(string).issubset(allowed_chars):
    #    return string
    #else:
    #	mensaje='caracter invalido '+str(string)
    #    log(mensaje)
    #    return ['error',mensaje]