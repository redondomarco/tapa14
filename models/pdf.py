# -*- coding: utf-8 -*-
#dependencias sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
#sudo pip install pdftotext tornado fpdf
import pdftotext

def analizo_fa(path_factura, **kwargs):
    #solo abro pdf
    #log('analizo '+str(path_factura))
    if path_factura[-4:]=='.pdf':
        with open(path_factura, "rb") as f:
            pdf = pdftotext.PDF(f)
        a=pdf[0]
        b=a.split('\n')
        c=[]
        salida={}
        for i in b:
            c.append(i.split())
        if 'debug' in kwargs.keys():
        	return c
	    #compruebo que la factura se ajuste
        if c[1][-2]==u'A':
            condiciones_a=[
            c[14]==[u'Subtotal', u'c/IVA'],
            c[-19]==[u'Otros', u'Tributos'],
            c[-7]==[u'Importe', u'Otros', u'Tributos:', u'$', u'0,00']
            ]
            for i in condiciones_a:
                if i==False:
                    return ['error','no cumple alguna condicion'+str(condiciones_a)]
            proceso=leo_fa_a(c)
            hash_md5=md5(path_factura)
            proceso[1]['md5']=hash_md5
            proceso[1]['nombre_archivo']=str(os.path.basename(path_factura))
            return proceso
        else:
            mensaje=path_factura+' formato desconocido'
            #log(mensaje)
            return ['error',mensaje]
    else:
        mensaje='archivo invalido: '+path_factura
        log(mensaje)
        return['error', mensaje]

# def leo_fa_a(c):
#     #analizo c
#     ##datos de la factura
#     salida={}
#     salida['f_copia']=tostring(c[0][0])
#     salida['f_nom_doc']=tostring(c[1][-1])
#     salida['f_tipo']=tostring(c[1][-2])
#     salida['f_cod']=tostring(c[2][-1])
#     salida['f_ptovta']=tostring(c[3][-4])
#     salida['f_nro']=tostring(c[3][-1])
#     salida['f_fechae']=tostring(c[4][-1])
#     #f_cae
#     #f_vtocae
#     salida['f_nrocodbar']=tostring(c[-2][0])
#     ##datos del emisor
#     salida['e_rsocial']=tostring(c[4][2:-4])
#     #
#     #armo domicilio multilinea
#     marca=c[6].index(u'Ingresos')
#     sda_parte=''
#     #if marca>0:
#     salida['e_domicilio']=tostring(c[5][2:-2])+sda_parte
#     salida['e_cuit']=tostring(c[5][-1])
#     salida['e_iibb']=tostring(c[6][-1])
#     marca=c[7].index(u'Fecha')
#     salida['e_condiva']=tostring(c[7][4:marca])
#     salida['e_fia']=tostring(c[7][-1])
#     #
#     ##datos del receptor
#     salida['r_cuit']=tostring(c[8][1])
#     marca=c[8].index(u'Social:')+1
#     salida['r_rsocial']=tostring(c[8][marca:])
#     marca1=c[9].index(u'IVA:')+1
#     marca2=c[9].index(u'Domicilio')
#     salida['r_condiva']=tostring(c[9][marca1:marca2])
#     marca=c[9].index(u'Comercial:')+1
#     salida['r_domicilio']=tostring(c[9][marca:])
#     salida['r_condvta']=tostring(c[10][-1])
#     ##detalle de la venta
#     #detecto primera linea
#     articulos=[]
#     marca_primera_linea=c.index([u'Subtotal', u'c/IVA'])+1
#     marca_segunda_linea=c.index([u'Subtotal', u'c/IVA'])+2
#     marca_ultima_linea=c.index([u'Otros', u'Tributos'])-1
#     #testeo si hay nota
#     #no hay nota si hay 'unidades' o 'docenas' en primera Y segunda linea'
#     if ('unidades' in str(c[marca_primera_linea])) or ('docenas' in str(c[marca_primera_linea])):
#         if ('unidades' in str(c[marca_segunda_linea])) or ('docenas' in str(c[marca_segunda_linea])):
#             salida['nota']=''
#             marca_segunda_linea=marca_primera_linea
#         elif marca_ultima_linea==marca_primera_linea:
#             #hay una sola linea
#             salida['nota']=''
#         else:
#             salida['nota']='hay nota'
#     elif ('unidades' in str(c[marca_primera_linea])) or ('docenas' in str(c[marca_primera_linea])):
#         if marca_ultima_linea==marca_primera_linea:
#             #hay una sola linea
#             salida['nota']=''
#         else:
#             salida['nota']='hay nota'
#     else:
#         salida['nota']='hay nota'
#     if salida['nota']!='':
#         #log('hay nota')
#         #hay nota-> identifico (producto + nota) + resto de columnas
#         try:
#             #supongo q la primera linea contiene resto de columnas-unidades
#             marca=c[marca_primera_linea].index(u'unidades')-1
#             salida['nota']=tostring(c[marca_primera_linea][0:marca])
#         except Exception as e1:
#             #log('e1 '+str(e1))
#             try:
#                 #la primera linea contiene resto de columnas-docenas
#                 marca=c[marca_primera_linea].index(u'docenas')-1
#                 salida['nota']=tostring(c[marca_segunda_linea][0:marca])
#             except Exception as e2:
#                 pass
#                 #log('e2 '+str(e2))
# 	 	try:
# 			#la segunda linea contiene resto de columnas
# 			marca=c[marca_segunda_linea].index(u'unidades')-1
# 			salida['nota']=tostring(c[marca_segunda_linea][0:marca])
# 		except Exception as e3:
# 			#log('e3 '+str(e3))
# 			try:
# 				#la segunda linea contiene resto de columnas
# 	 			marca=c[marca_segunda_linea].index(u'docenas')-1
# 	 			salida['nota']=tostring(c[marca_segunda_linea][0:marca])
# 	 		except Exception as e4:
# 	 			#log('e4 '+str(e4))
# 	 			pass
# 	 	#armo primer articulo
# 	#armo primer articulo para facturas con nota detecto linea.
# 	if salida['nota']!='':
# 		#log('tiene nota')
# 		articulos=[[
# 		'',
# 		tostring(c[marca_primera_linea+1]),
# 		tostring(c[marca_primera_linea][-7]),
# 		tostring(c[marca_primera_linea][-6]),
# 		tostring(c[marca_primera_linea][-5]),
# 		tostring(c[marca_primera_linea][-4]),
# 		tostring(c[marca_primera_linea][-3]),
# 		tostring(c[marca_primera_linea][-2]),
# 		tostring(c[marca_primera_linea][-1])]]
# 		rango=range(marca_segunda_linea+1,marca_ultima_linea)
# 	else:
# 		#no tiene nota arranco por el primer elemento
# 		rango=range(marca_primera_linea,marca_ultima_linea)
# 		if rango==[]:
# 			#para el caso de un articulo
# 			rango=[marca_primera_linea]
# 	#proceso resto de articulos
# 	for n in rango:
# 		#cod,prod,cant,umed,puni,boni,subt,alic,suci
# 		cod=''
# 		prod=tostring(c[n][0:-7])
# 		cant=tostring(c[n][-7])
# 		umed=tostring(c[n][-6])
# 		puni=tostring(c[n][-5])
# 		boni=tostring(c[n][-4])
# 		subt=tostring(c[n][-3])
# 		alic=tostring(c[n][-2])
# 		suci=tostring(c[n][-1])
# 		articulos.append([cod,prod,cant,umed,puni,boni,subt,alic,suci])
# 	salida['d_art']=articulos
# 	#datos de importes
# 	#it_siva
# 	#it_iva
# 	salida['it_total']=tostring(c[-6][3])
# 	return ['ok',salida]

# def leo_fa_b(c):
# 	#analizo c
# 	##datos de la factura
# 	salida={}
# 	salida['f_copia']=tostring(c[0][0])
# 	salida['f_nom_doc']=tostring(c[1][-1])
# 	salida['f_tipo']=tostring(c[1][-2])
# 	salida['f_cod']=tostring(c[2][-1])
# 	salida['f_ptovta']=tostring(c[3][-4])
# 	salida['f_nro']=tostring(c[3][-1])
# 	salida['f_fechae']=tostring(c[4][-1])
# 	#f_cae
# 	#f_vtocae
# 	salida['f_nrocodbar']=tostring(c[-2][0])
# 	##datos del emisor
# 	salida['e_rsocial']=tostring(c[4][2:-4])
# 	#
# 	#armo domicilio multilinea
# 	marca=c[6].index(u'Ingresos')
# 	sda_parte=''
# 	if marca>0:
# 		sda_parte=' '+tostring(c[6][0:marca])
# 	salida['e_domicilio']=tostring(c[5][2:-2])+sda_parte
# 	salida['e_cuit']=tostring(c[5][-1])
# 	salida['e_iibb']=tostring(c[6][-1])
# 	marca=c[7].index(u'Fecha')
# 	salida['e_condiva']=tostring(c[7][4:marca])
# 	salida['e_fia']=tostring(c[7][-1])
# 	#
# 	##datos del receptor
# 	salida['r_cuit']=tostring(c[8][1])
# 	marca=c[8].index(u'Social:')+1
# 	salida['r_rsocial']=tostring(c[8][marca:])
# 	marca1=c[9].index(u'IVA:')+1
# 	marca2=c[9].index(u'Domicilio:')
# 	salida['r_condiva']=tostring(c[9][marca1:marca2])
# 	#marca=c[9].index(u'Comercial:')+1
# 	salida['r_domicilio']=tostring(c[9][marca2+1:])
# 	salida['r_condvta']=tostring(c[10][-1])
# 	##detalle de la venta
# 	#detecto primera linea
# 	articulos=[]
# 	marca_primera_linea=c.index([u'Subtotal', u'c/IVA'])+1
# 	marca_segunda_linea=c.index([u'Subtotal', u'c/IVA'])+2
# 	marca_ultima_linea=c.index([u'Otros', u'Tributos'])-1
# 	#testeo si hay nota
# 	#no hay nota si hay 'unidades' o 'docenas' en primera Y segunda linea'
# 	if ('unidades' in str(c[marca_primera_linea])) or ('docenas' in str(c[marca_primera_linea])):
# 		if ('unidades' in str(c[marca_segunda_linea])) or ('docenas' in str(c[marca_segunda_linea])):
# 			salida['nota']=''
# 			marca_segunda_linea=marca_primera_linea
# 		elif marca_ultima_linea==marca_primera_linea:
# 			#hay una sola linea
# 			salida['nota']=''
# 		else:
# 			salida['nota']='hay nota'
# 	elif ('unidades' in str(c[marca_primera_linea])) or ('docenas' in str(c[marca_primera_linea])):
# 		if marca_ultima_linea==marca_primera_linea:
# 			#hay una sola linea
# 			salida['nota']=''
# 		else:
# 			salida['nota']='hay nota'
# 	else:
# 		salida['nota']='hay nota'
# 	if salida['nota']!='':
# 		#log('hay nota')
# 		#hay nota-> identifico (producto + nota) + resto de columnas
# 		try:
# 			#supongo q la primera linea contiene resto de columnas-unidades
# 			marca=c[marca_primera_linea].index(u'unidades')-1
# 			salida['nota']=tostring(c[marca_primera_linea][0:marca])
# 		except Exception as e1:
# 			#log('e1 '+str(e1))
# 			try:
# 				#la primera linea contiene resto de columnas-docenas
# 	 			marca=c[marca_primera_linea].index(u'docenas')-1
# 	 			salida['nota']=tostring(c[marca_segunda_linea][0:marca])
# 	 		except Exception as e2:
# 	 			#log('e2 '+str(e2))
# 	 			pass
# 	 	try:
# 			#la segunda linea contiene resto de columnas
# 			marca=c[marca_segunda_linea].index(u'unidades')-1
# 			salida['nota']=tostring(c[marca_segunda_linea][0:marca])
# 		except Exception as e3:
# 			#log('e3 '+str(e3))
# 			try:
# 				#la segunda linea contiene resto de columnas
# 	 			marca=c[marca_segunda_linea].index(u'docenas')-1
# 	 			salida['nota']=tostring(c[marca_segunda_linea][0:marca])
# 	 		except Exception as e4:
# 	 			#log('e4 '+str(e4))
# 	 			pass
# 	 	#armo primer articulo
# 	#armo primer articulo para facturas con nota detecto linea.
# 	if salida['nota']!='':
# 		#log('tiene nota')
# 		articulos=[[
# 		'',
# 		tostring(c[marca_primera_linea+1]),
# 		tostring(c[marca_primera_linea][-7]),
# 		tostring(c[marca_primera_linea][-6]),
# 		tostring(c[marca_primera_linea][-5]),
# 		tostring(c[marca_primera_linea][-4]),
# 		tostring(c[marca_primera_linea][-3]),
# 		tostring(c[marca_primera_linea][-2]),
# 		tostring(c[marca_primera_linea][-1])]]
# 		rango=range(marca_segunda_linea+1,marca_ultima_linea)
# 	else:
# 		#no tiene nota arranco por el primer elemento
# 		rango=range(marca_primera_linea,marca_ultima_linea)
# 		if rango==[]:
# 			#para el caso de un articulo
# 			rango=[marca_primera_linea]
# 	#proceso resto de articulos
# 	for n in rango:
# 		#cod,prod,cant,umed,puni,boni,subt,alic,suci
# 		cod=''
# 		prod=tostring(c[n][0:-7])
# 		cant=tostring(c[n][-7])
# 		umed=tostring(c[n][-6])
# 		puni=tostring(c[n][-5])
# 		boni=tostring(c[n][-4])
# 		subt=tostring(c[n][-3])
# 		alic=tostring(c[n][-2])
# 		suci=tostring(c[n][-1])
# 		articulos.append([cod,prod,cant,umed,puni,boni,subt,alic,suci])
# 	salida['d_art']=articulos
# 	#datos de importes
# 	#it_siva
# 	#it_iva
# 	salida['it_total']=tostring(c[-6][3])
# 	return ['ok',salida]

# def test_fa_b():
# 	c=analizo_fa(base_dir+'/errores/20143513972_006_00004_00000178.pdf', debug=True)
# 	aux=leo_fa_b(c)
# 	return aux


def tostring(argumento):
	"""list of unicodes to string with spaces"""
	#log(argumento)
	if type(argumento)==list:
		str_result=''
		for i in argumento:
			str_result=str_result+i.encode('utf8')+' '
		return str_result[0:-1]
	elif type(argumento)==unicode:
		return argumento.encode('utf8')

from os import walk
def test_leo():
	dir, subdirs, archivos = next(walk('applications/dev/files/facturas/'))
	resultado=[]
	for factura in archivos:
		#log('analizo: '+dir+factura)
		fleida=analizo_fa(dir+factura)
		if fleida[0]=='error':
			log('error con factura: '+str(factura))
		else:
			resultado.append(fleida[1])
	return resultado

def leo_para_despacho():
	dir, subdirs, archivos = next(walk('applications/dev/files/facturas/'))
	resultado=[]
	for factura in archivos:
		#log('analizo: '+dir+factura)
		fleida=analizo_fa(dir+factura)
		if fleida[0]=='error':
			#log('error con factura: '+str(factura))
			pass
		else:
			for articulo in fleida[1]['d_art']:
				producto=mapeo_prod(articulo[1])[1]
				fecha=fleida[1]['f_fechae']
				lote=busca_lote(fecha,producto)
				aux={
				'producto':producto,
				'cant':articulo[2],
				'fa_n':fleida[1]['f_nro'],
				'fecha':fleida[1]['f_fechae'],
				'cliente':fleida[1]['r_rsocial'],
				'lote':lote,
				#'md5':fleida[1]['md5'],
				#'nota':fleida[1]['nota']
				}
				resultado.append(aux)
			#resultado.append(fleida[1])
	log('fin proceso leer facturas')
	return resultado

# descripcion biblioteca
# directorio raiz /home/$user/web2py/application/$app/files
# upload -> directorio donde subo archivos a procesar
# errores -> archivos procesados con errores
# duplicados -> archivos duplicados
# csv -> informes sueltos en csv
# pdf/
#   /%año/%mes/%dia/
#                   nv -> notas de venta
#                   fa -> facturas+csv de los pdf que contiene la carpeta
#                   re -> registro de elaboracion
#                   rd -> registro de despacho

base_dir='applications/'+str(myconf.take('datos.app_name'))+'/files'

import shutil
def proceso_fa():
	#intento leer facturas en directorio x
	#segun fecha, tipo, hash
	# * si el hash esta duplicado descarto el archivo
	# * si hay errores muevo a carpeta 'errores'
	# * intento mover a la biblioteca (creo carpetas)
	#si se agregaron archivos genero csv del contenido del directorio
	dir_origen='/facturas/'
	dir, subdirs, archivos = next(walk(base_dir+dir_origen))
	resultado=[]
	for factura in archivos:
		#log('analizo: '+dir+factura)
		fleida=analizo_fa(dir+factura)
		if fleida[0]=='error':
			log('error con factura: '+str(factura))
			shutil.move(
				base_dir+dir_origen+factura,
				base_dir+'/errores/'+factura)
			log('movido '+str(factura))
		else:
			resultado.append(fleida[1])
	for i in resultado:
		fecha_dir=i['f_fechae'].split('/')
		dir_dest=base_dir+'/pdf/'+str(fecha_dir[2])+'/'+str(fecha_dir[1])+'/'+str(fecha_dir[0])+'/fa/'
		file_orig=base_dir+dir_origen+i['nombre_archivo']
        #intento creo directorio si no existe
		try:
			os.makedirs(dir_dest)
		except:
			pass
		#intento abrir csv si existe
		try:
			lista=open(directorio+'/archivos.csv', 'r').read().split()
		except Exception as e:
			lista=[]
		if i['md5'] in str(lista):
			shutil.move(
				file_orig,
				base_dir+dir_origen+'/duplicados/'+i['nombre_archivo'])
		else:
			#considero que no esta en la carpeta, muevo el archivo
			shutil.move(
				file_orig,
				dir_dest+i['nombre_archivo'])
			log('movido '+str(file_orig))
			aux=genero_csv_dir(dir_dest)

def genero_csv_dir(dir):
	dir, subdirs, archivos = next(walk(dir))
	resultado=[]
	#proceso solo pdfs
	for i in archivos:
		if i[-3:]!='pdf':
			archivos.remove(i)
	log(archivos)
	for factura in archivos:
		#log('analizo: '+dir+factura)
		fleida=analizo_fa(dir+factura)
		if fleida[0]=='error':
			log('error con factura: '+str(factura))
			log('aqui no deberia haber error!!!!')
		else:
			resultado.append(fleida[1])
	nombre_csv='infodir'+str(dir)[27:37].replace('/','-')
	return list_of_dict_to_csv(nombre_csv,resultado, dir=dir, norandom='yes')

#funciones para despacho
def mapeo_prod(producto):
	minus=str(producto).lower()
	#dc
	if all(['empanada' in minus, 'criolla' in minus, '123' in minus, '18' in minus]):
		return [producto,'TDC123x18']
	#dh
	elif all(['empanada' in minus, 'hojaldre' in minus, '123' in minus, '18' in minus]):
		return [producto,'TDH123x18']
	#pc
	elif all(['pascualina' in minus, 'criolla' in minus, '300' in minus, '16' in minus]):
		return [producto,'TPC300x16']
	#ph
	elif all(['pascualina' in minus, 'hojaldre' in minus, '300' in minus, '16' in minus]):
		return [producto,'TPH300x16']
	#rc
	elif all(['rotisero' in minus, 'criollo' in minus, '135' in minus, '12' in minus]):
		return [producto,'TRC135x12']
	#rh
	elif all(['otisero' in minus, 'hojaldre' in minus, '135' in minus, '12' in minus]):
		return [producto,'TRH135x12']
	#rc135 cat
	elif all(['rotisero' in minus, 'criollo' in minus, '135' in minus]):
		return [producto,'TRC135xDOC']
	#rh147 cat
	elif all(['super' in minus, 'rotisero' in minus, '147' in minus]):
		return [producto,'TRH147xDOC']
	#rh160 cat
	elif all(['rotisero' in minus, 'hojaldre' in minus, '160' in minus]):
		return [producto,'TRH160xDOC']

	# minit
	elif all(['mini' in minus, 'hojaldre' in minus, '220' in minus]):
		return [producto,'MTH220']
	
	#copetin varios
	elif all(['copetin' in minus, 'criollo' in minus]):
		return [producto,'TDC123x18']
		#return [producto,'TCHxDOC']
	elif all(['copetin' in minus, 'criollo' in minus]):
		return [producto,'TDC123x18']
		#return [producto,'TCHxDOC']

	#errores granbai
	elif any([
		'dow' in minus, 'jd' in minus, 'cp' in minus, 'deere' in minus,
		'rotiser/o' in minus, 'em/panada' in minus, 'tapa_empanada_criolla' in minus]):
		return [producto,'TRH135x12']

	#panin
	elif all(['discos' in minus, 'freir' in minus, '123' in minus, '12' in minus]):
		return [producto,'PNN123DC']
	elif all(['discos' in minus, 'horno' in minus, '123' in minus, '12' in minus]):
		return [producto,'PNN123DH']
	elif all(['pascualina' in minus, 'criolla' in minus, '300' in minus, '2' in minus]):
		return [producto,'PNN300PC']
	elif all(['pascualina' in minus, 'hojaldre' in minus, '300' in minus, '2' in minus]):
		return [producto,'PNN300PH']
	else:
		log(str(producto)+' sin etiqueta')
		return[producto,producto]

def busca_lote(fechaf,producto):
	lotes=[]
	fechafa=datetime.strptime(fechaf,'%d/%m/%Y')
	csvleido=open(base_dir+'/csv/elaboracion/elab_1-04-208_al_7-11-2018.csv', 'r').read().split()
	lista=[]
	#formateo csv
	for i in csvleido:
		aux=i.split(',')
		fecha=datetime.strptime(aux[0],'%Y/%m/%d')
		prod=aux[1]
		lote=aux[2]
		lista.append([fecha,prod,lote])
	#return lista
	n=1
	while lotes==[]:
		lotes=sub_busca_lote(lista,n,producto,fechafa)
		n+=1
		if n==30:
			log('algo esta mal')
			break
	return list(set(lotes))

def sub_busca_lote(lista,dias,producto,fechafa):
	lotes=[]
	for i in lista:
		if i[1]==producto:
			#si la fecha de elboracion es X dias o menos de la fecha de la factura lo agrego
			if all([ i[0]>=(fechafa-timedelta(days=dias)), i[0]<=fechafa]):
				lotes.append(i[2])
	return lotes
