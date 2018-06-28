# -*- coding: iso-8859-1 -*-
#Actualizado 24/08/2012
import os
from fpdf import FPDF

def generar_factura_test():
	hoy=datetime.today()
	directorio='applications/'+str(myconf.take('datos.app_name'))+'/pdf/'+str(hoy.year)+'/'+str(hoy.month)+'/'+str(hoy.day)
	try:
		os.makedirs(directorio)
	except:
		pass
	pdf = FPDF()
	pdf.add_page(orientation='P')
	pdf.set_font('arial', '', 13.0)
	pdf.set_xy(105.0, 8.0)

	pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt='Orden de Venta', border=0)
	pdf.set_line_width(1.0)
	pdf.rect(15.0, 15.0, 170.0, 245.0)
	pdf.set_line_width(0.0)
	pdf.rect(95.0, 15.0, 10.0, 10.0)
	#descomentar para poner imagen de la serpiente
	#pdf.image('serpiente.png', 20.0, 17.0, link='', type='', w=13.0, h=13.0)
	pdf.set_font('arial', 'B', 16.0)
	pdf.set_xy(95.0, 18.0)
	pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt='X', border=0)
	pdf.set_font('arial', '', 8.0)
	pdf.set_xy(105.0, 21.0)
	pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
	pdf.set_font('arial', 'B', 7.0)
	pdf.set_xy(95.0, 21.5)
	pdf.cell(ln=0, h=4.5, align='C', w=10.0, txt='COD.00', border=0)
	pdf.set_line_width(0.0)
	pdf.line(100.0, 25.0, 100.0, 57.0)
	pdf.set_font('arial', 'B', 14.0)
	pdf.set_xy(125.0, 25.5)
	pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
	pdf.set_xy(115.0, 27.5)
	pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='N\xba: ', border=0)
	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(17.0, 32.5)
	pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt=' ', border=0)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(115.0, 33.0)
	pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
	pdf.set_xy(135.0, 33.0)
	pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt='8/02/2018', border=0)
	pdf.set_line_width(0.1)
	pdf.line(15.0, 57.0, 185.0, 57.0)
	pdf.set_font('arial', '', 10.0)
	pdf.set_xy(17.0, 59.0)
	pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
	pdf.set_xy(35.0, 59.0)
	pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt='Cancelliero', border=0)
	pdf.set_xy(17.0, 64.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Domicilio:', border=0)
	pdf.set_xy(35.0, 64.0)
	pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt='Uriburu y Bb As', border=0)
	pdf.set_xy(17.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt=' ', border=0)
	pdf.set_xy(35.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt='-', border=0)
	pdf.set_xy(115.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
	pdf.set_xy(133.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt='Rosario', border=0)
	pdf.set_line_width(0.0)
	pdf.line(15.0, 77.0, 185.0, 77.0)
	pdf.set_xy(17.0, 80.0)
	pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt=' ', border=0)
	pdf.set_xy(35.0, 80.0)
	pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt=' ', border=0)
	pdf.set_xy(115.0, 80.0)
	pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt=' ', border=0)
	pdf.set_xy(135.0, 80.0)
	pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt=' ', border=0)
	pdf.set_line_width(0.0)
	pdf.line(15.0, 88.0, 185.0, 88.0)
	pdf.set_xy(17.0, 90.0)
	pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Condiciones Pago:', border=0)
	pdf.set_xy(65.0, 90.0)
	pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='Contado', border=0)
	pdf.set_xy(92.0, 90.0)
	pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Per\xedodo Facturado', border=0)
	pdf.set_xy(125.0, 90.0)
	pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='01/01/2009', border=0)
	pdf.set_xy(150.0, 90.0)
	pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='31/01/2009', border=0)
	pdf.set_line_width(0.0)
	pdf.line(15.0, 95.0, 185.0, 95.0)
	pdf.set_line_width(0.0)
	pdf.line(155.0, 95.0, 155.0, 230.0)
	pdf.set_xy(20.0, 97.0)
	pdf.cell(ln=0, h=5.0, align='L', w=125.0, txt='Descripci\xf3n', border=0)
	pdf.set_xy(160.0, 97.0)
	pdf.cell(ln=0, h=5.0, align='R', w=20.0, txt='Importe', border=0)
	pdf.set_line_width(0.0)
	pdf.line(15.0, 102.0, 185.0, 102.0)
	pdf.set_xy(20.0, 103.0)
	pdf.cell(ln=0, h=7.0, align='L', w=125.0, txt='Esto es una prueba y no es v\xe1lido como factura', border=0)
	pdf.set_xy(160.0, 103.0)
	pdf.cell(ln=0, h=7.0, align='R', w=20.0, txt='100,00', border=0)
	pdf.set_line_width(0.0)
	pdf.line(15.0, 230.0, 185.0, 230.0)
	pdf.set_xy(20.0, 233.0)
	pdf.cell(ln=0, h=5.0, align='L', w=95.0, txt='CAE N\xba', border=0)
	pdf.set_xy(45.0, 233.0)
	pdf.cell(ln=0, h=5.0, align='L', w=30.0, txt='01234567890', border=0)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(105.0, 234.0)
	pdf.cell(ln=0, h=9.0, align='R', w=45.0, txt='NETO GRAVADO:', border=0)
	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(145.0, 234.0)
	pdf.cell(ln=0, h=9.0, align='R', w=33.0, txt='100,00', border=0)
	pdf.set_font('arial', '', 10.0)
	pdf.set_xy(20.0, 238.0)
	pdf.cell(ln=0, h=5.0, align='L', w=95.0, txt='Fecha Vto. CAE:', border=0)
	pdf.set_xy(55.0, 238.0)
	pdf.cell(ln=0, h=5.0, align='L', w=30.0, txt='19/02/2009', border=0)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(125.0, 241.0)
	pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='IVA 21%:', border=0)
	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(145.0, 241.0)
	pdf.cell(ln=0, h=9.0, align='R', w=33.0, txt='21,00', border=0)
	pdf.interleaved2of5('012345678905', 20.0, 243.5, w=0.75)
	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(105.0, 251.0)
	pdf.cell(ln=0, h=9.0, align='R', w=73.0, txt='121,00', border=0)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(125.0, 251.0)
	pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)
	pdf.set_line_width(0.0)
	pdf.rect(155.0, 252.0, 25.0, 7.0)
	pdf.set_font('arial', '', 10.0)
	pdf.set_xy(20.0, 253.0)
	pdf.cell(ln=0, h=7.0, align='L', w=120.0, txt='012345678905', border=0)
	#documento=directorio+'/test-factura-'+str(hoy.isoformat())+'.pdf'
	documento=directorio+'/test.pdf'
	pdf.output(documento, 'F')
	log('documento en: '+str(documento))
	return documento
	#os.system("test-factura.pdf")

def busca_nv(pedidonum):
	lista_archivos=[]
	for root, directories, filenames in os.walk(dir_pdf):
		for filename in filenames:
			lista_archivos.append([os.path.join(root),os.path.join(filename)])
	for i in lista_archivos:
		if pedidonum==i[1]:
			return ['ok',i[0]+'/'+i[1]]
	return ['error','no existe']

def gestiona_nv(pedidonum):
	comprobante='nv_'+str(pedidonum)
	#compruebo si existe el comprobante
	aux=busca_nv(comprobante)
	if aux[0]=='ok':
		return aux[1]
	else:
		#genero nv
		hoy=datetime.today()
		dir_fecha=str(hoy.year)+'/'+str(hoy.month)+'/'+str(hoy.day)
		directorio=dir_pdf+dir_fecha+'/nv/'
		try:
			os.makedirs(directorio)
		except:
			pass
		genera_nv(fecha,comprobante,pedidonum,items,directorio)

#nota de venta
#fecha
#nro comprobante
#cliente
#item: producto,unitario,cantidad
def genera_nv(fecha,pedidonum,clienteid,items,directorio,nota):
	datos_cliente=obtengo_cliente(clienteid)
	comprobante='nv_'+str(pedidonum)
	pdf = FPDF()
	pdf.add_page(orientation='P')
	
	#recuadro contenedor
	pdf.set_line_width(1.0)
	pdf.rect(15.0, 15.0, 170.0, 245.0)
	#recuadro original-duplicado
	pdf.set_line_width(0.0)
	pdf.rect(15.0, 15.0, 170.0, 10.0)

	#recuadro copia documento
	pdf.set_line_width(0.0)
	pdf.rect(95.0, 25.0, 10.0, 10.0)
	#copia documento
	pdf.set_xy(95.0, 19.0)
	pdf.set_font('arial', 'B', 14.0)
	pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt='ORIGINAL', border=0)

	#letra
	pdf.set_xy(95.0, 29.0)
	pdf.set_font('arial', 'B', 16.0)
	pdf.cell(ln=0, h=3.0, align='C', w=10.0, txt='X', border=0)

	#divisor cabecera
	pdf.set_line_width(0.0)
	pdf.line(100.0, 35.0, 100.0, 57.0)

	#Titulo Documento
	pdf.set_font('arial', '', 16.0)
	pdf.set_xy(115.0, 20.0)
	pdf.cell(ln=0, h=26.0, align='C', w=75.0, txt='Nota de Venta', border=0)

	#bloque datos emisor
	#descomentar para poner imagen
	#pdf.image('applications/dev/static/images/tapa14-bn-20p.jpg', 20.0, 30.0, link='', type='', w=20.0, h=20.0)
	pdf.image('applications/dev/static/images/rosarioigual.png', 20.0, 30.0, link='', type='', w=20.0, h=20.0)
	
	#pdf.set_font('arial', '', 8.0)
	#pdf.set_xy(105.0, 21.0)
	#pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
	#codigo tipo doc
	#pdf.set_font('arial', 'B', 7.0)
	#pdf.set_xy(95.0, 21.5)
	#pdf.cell(ln=0, h=4.5, align='C', w=10.0, txt='COD.00', border=0)
	
	#numero pedido
	pdf.set_font('arial', 'B', 14.0)
	pdf.set_xy(135.0, 37.5)
	pdf.cell(ln=0, h=9.5, align='L', w=10.0, txt='N\xba', border=0)
	pdf.set_xy(145.0, 37.5)
	pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt=str(pedidonum).zfill(10), border=0)
	
	
	#pdf.set_font('arial', 'B', 12.0)
	#pdf.set_xy(17.0, 32.5)
	#pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt=' ', border=0)
	
	#fecha
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(135.0, 45.0)
	pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
	pdf.set_xy(155.0, 45.0)
	pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(fecha), border=0)
	
	#divisor 1 cliente
	#pdf.set_line_width(0.1)
	#pdf.line(15.0, 57.0, 185.0, 57.0)
	#pdf.set_line_width(0.0)
	#pdf.line(15.0, 77.0, 185.0, 77.0)
	#recuadro cliente
	pdf.set_line_width(0.0)
	pdf.rect(15.0, 57.0, 170.0, 20.0)

	#datos cliente
	pdf.set_font('arial', '', 10.0)
	pdf.set_xy(17.0, 59.0)
	pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
	pdf.set_xy(35.0, 59.0)
	pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=str(datos_cliente['razon_social']), border=0)
	pdf.set_xy(17.0, 64.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Domicilio:', border=0)
	pdf.set_xy(35.0, 64.0)
	pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=str(datos_cliente['domicilio']), border=0)
	pdf.set_xy(17.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Condicion de venta:', border=0)
	pdf.set_xy(55.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=quito_ce(datos_cliente['tipocuenta']).capitalize(), border=0)
	pdf.set_xy(110.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
	pdf.set_xy(130.0, 69.0)
	pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=str(datos_cliente['localidad'])+', '+str(datos_cliente['provincia']), border=0)
	
	#detalle
	#recuadro encabezados
	pdf.set_line_width(0.0)
	pdf.rect(15.0, 77.0, 170.0, 8.0)
	#codigo
	pdf.set_xy(17.0, 79.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='C\xf3digo', border=0)	
	pdf.line(32.0, 77.0, 32.0, 85.0)

	#producto
	pdf.set_xy(36.0, 79.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Producto', border=0)	
	pdf.line(100.0, 77.0, 100.0, 85.0)

	#cantidad
	pdf.set_xy(102.0, 79.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Cantidad', border=0)	
	pdf.line(120.0, 77.0, 120.0, 85.0)

	#punitario
	pdf.set_xy(122.0, 79.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Precio Unitario', border=0)	
	pdf.line(150.0, 77.0, 150.0, 85.0)


	#subtotal
	pdf.set_xy(160.0, 79.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='SubTotal', border=0)	
	
	#nota
	pdf.set_xy(36.0, 88.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)	

	
	#pdf.set_xy(36.0, 93.0)
	#pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)
	
	#items separados 6pts
	#primero pdf.set_xy(36.0, 93.0)
	renglon=94.0
	col_producto=36.0
	col_cant=108
	col_punit=128
	col_subt=153
	paso=5
	total=0
	log(items)
	for i in items:
		parcial=i[0][0]*i[0][2]
		pdf.set_xy(col_producto,renglon)
		pdf.cell(ln=0, h=4.0, align='L', w=60.0, txt=str(i[0][1]), border=0)
		pdf.set_xy(col_cant,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=10.0, txt=str(i[0][0]), border=0)
		pdf.set_xy(col_punit,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=20.0, txt=str(i[0][2]), border=0)
		pdf.set_xy(col_subt,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=30.0, txt=str(parcial), border=0)
		renglon=renglon+paso
		total=total+parcial
	
	pdf.set_line_width(0.0)
	pdf.line(15.0, 250.0, 185.0, 250.0)
	
	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(105.0, 251.0)
	pdf.cell(ln=0, h=9.0, align='R', w=73.0, txt=str(total), border=0)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(125.0, 251.0)
	pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)
	pdf.set_line_width(0.0)
	pdf.rect(155.0, 252.0, 25.0, 7.0)
	pdf.set_font('arial', '', 10.0)
	documento=directorio+str(comprobante)+'.pdf'
	pdf.output(documento, 'F')
	log('documento en: '+str(documento))
	return documento

def genera_nv1(fecha,pedidonum,clienteid,items,directorio,nota):
	datos_cliente=obtengo_cliente(clienteid)
	comprobante='nv_'+str(pedidonum)
	pdf = FPDF()
	pdf.add_page(orientation='P')
	
	#hoja1
	#recuadro contenedor
	pdf.set_line_width(1.0)
	pdf.rect(25.0, 15.0, 170.0, 130.0)
	#recuadro original-duplicado
	pdf.set_line_width(0.0)
	pdf.rect(25.0, 15.0, 170.0, 10.0)

	#recuadro copia documento
	pdf.set_line_width(0.0)
	pdf.rect(105.0, 25.0, 10.0, 10.0)
	#copia documento
	pdf.set_xy(105.0, 19.0)
	pdf.set_font('arial', 'B', 14.0)
	pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt='ORIGINAL', border=0)

	#letra
	pdf.set_xy(105.0, 29.0)
	pdf.set_font('arial', 'B', 16.0)
	pdf.cell(ln=0, h=3.0, align='C', w=10.0, txt='X', border=0)

	#divisor cabecera
	pdf.set_line_width(0.0)
	pdf.line(110.0, 35.0, 110.0, 53.0)	

	#Titulo Documento
	pdf.set_font('arial', '', 16.0)
	pdf.set_xy(125.0, 18.0)
	pdf.cell(ln=0, h=26.0, align='C', w=75.0, txt='Nota de Venta', border=0)

	#bloque datos emisor
	#descomentar para poner imagen
	#pdf.image('applications/dev/static/images/tapa14-bn-20p.jpg', 20.0, 30.0, link='', type='', w=20.0, h=20.0)
	pdf.image('applications/dev/static/images/rosarioigual.png', 30.0, 30.0, link='', type='', w=20.0, h=20.0)
	
	#numero pedido
	pdf.set_font('arial', 'B', 14.0)
	pdf.set_xy(134.0, 35)
	pdf.cell(ln=0, h=9.5, align='L', w=10.0, txt='N\xba', border=0)
	pdf.set_xy(142.0, 35)
	pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt=str(pedidonum).zfill(10), border=0)
	
	#fecha
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(134.0, 43.0)
	pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
	pdf.set_xy(154.0, 43.0)
	pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(fecha), border=0)
	
	#recuadro cliente
	pdf.set_line_width(0.0)
	pdf.rect(25.0, 53.0, 170.0, 20.0)

	#datos cliente
	pdf.set_font('arial', '', 10.0)
	pdf.set_xy(27.0, 55.0)
	pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
	pdf.set_xy(45.0, 55.0)
	pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt=str(datos_cliente['razon_social']), border=0)
	pdf.set_xy(27.0, 60.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Domicilio:', border=0)
	pdf.set_xy(45.0, 60.0)
	pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt=str(datos_cliente['domicilio']), border=0)
	pdf.set_xy(27.0, 65.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Condicion de venta:', border=0)
	pdf.set_xy(65.0, 65.0)
	pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt=quito_ce(datos_cliente['tipocuenta']).capitalize(), border=0)
	pdf.set_xy(120.0, 65.0)
	pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
	pdf.set_xy(140.0, 65.0)
	pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt=str(datos_cliente['localidad'])+', '+str(datos_cliente['provincia']), border=0)
	
	#detalle
	col_codigo=27
	col_producto=46.0
	col_cant=118
	col_punit=138
	col_subt=163

	#recuadro encabezados
	pdf.set_line_width(0.0)
	pdf.rect(25.0, 73.0, 170.0, 8.0)
	#codigo
	pdf.set_xy(col_codigo, 75.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='C\xf3digo', border=0)	
	pdf.line(col_codigo+17, 73.0, col_codigo+17, 81.0)

	#producto
	pdf.set_xy(col_producto, 75.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Producto', border=0)	
	pdf.line(col_producto+70, 73.0, col_producto+70, 81.0)

	#cantidad
	pdf.set_xy(col_cant, 75.0)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Cantidad', border=0)	
	pdf.line(col_cant+18, 73.0, col_cant+18, 81.0)

	#punitario
	pdf.set_xy(col_punit, 75.0)
	pdf.cell(ln=0, h=4.0, align='R', w=25.0, txt='Precio Unitario', border=0)	
	pdf.line(col_punit+28, 73.0, col_punit+28, 81.0)


	#subtotal
	pdf.set_xy(col_subt, 75.0)
	pdf.cell(ln=0, h=4.0, align='R', w=28.0, txt='SubTotal', border=0)	
	
	#nota
	renglon=84
	ult_renglon=135
	pdf.set_xy(col_producto, renglon)
	pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)	
	renglon=renglon+6
	
	#pdf.set_xy(36.0, 93.0)
	#pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)
	
	#items separados 6pts
	#primero pdf.set_xy(36.0, 93.0)
	

	paso=5
	total=0
	log(items)
	for i in items:
		parcial=i[0][0]*i[0][2]
		pdf.set_xy(col_producto,renglon)
		pdf.cell(ln=0, h=4.0, align='L', w=60.0, txt=str(i[0][1]), border=0)
		pdf.set_xy(col_cant,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=10.0, txt=str(i[0][0]), border=0)
		pdf.set_xy(col_punit,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=20.0, txt=str(i[0][2]), border=0)
		pdf.set_xy(col_subt,renglon)
		pdf.cell(ln=0, h=4.0, align='R', w=30.0, txt=str(parcial), border=0)
		renglon=renglon+paso
		total=total+parcial
	
	pdf.set_line_width(0.0)
	pdf.line(25.0, 132.0, 195.0, 132.0)
	


	pdf.set_font('arial', 'B', 12.0)
	pdf.set_xy(col_subt, ult_renglon)
	pdf.cell(ln=0, h=9.0, align='R', w=30.0, txt=str(total), border=1)
	pdf.set_font('arial', '', 12.0)
	pdf.set_xy(col_punit, ult_renglon)
	pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)

	#divisor
	pdf.set_line_width(0.0)
	pdf.line(5, 148.5, 205.0, 148.5)

	#hoja2
	#recuadro contenedor
	pdf.set_line_width(1.0)
	pdf.rect(15.0, 160.0, 170.0, 130.0)
	#recuadro original-duplicado
	#pdf.set_line_width(0.0)
	#pdf.rect(15.0, 15.0, 170.0, 10.0)



	documento=directorio+str(comprobante)+'.pdf'
	pdf.output(documento, 'F')
	log('documento en: '+str(documento))
	return documento


def test_genera_nv():
	pedidonum=30
	test=obtengo_pedido(pedidonum)
	if test[1]==None:
		fecha='19/6/2018'
	else:
		fecha=str(test[1].day)+'/'+str(test[1].month)+'/'+str(test[1].year)
	clienteid=test[0]
	nota=test[2]
	items=test[3]
	#directorio='applications/dev/pdf/2018/6/19/nv/'
	directorio='applications/dev/pdf/test/nv/'
	try:
		os.makedirs(directorio)
	except:
		pass
	return genera_nv1(fecha,pedidonum,clienteid,items,directorio,nota)
