# -*- coding: utf-8 -*-
import os
from fpdf import FPDF

# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    from db import *
    from util import *


def busca_nv(pedidonum):
    lista_archivos = []
    for root, directories, filenames in os.walk(files_dir + 'pdf/'):
        for filename in filenames:
            lista_archivos.append([os.path.join(root), os.path.join(filename)])
    for i in lista_archivos:
        if pedidonum == i[1]:
            return ['ok', i[0] + '/' + i[1]]
    return ['error', 'no existe']


def gestiona_nv(pedidonum):
    comprobante = 'nv_' + str(pedidonum)
    # compruebo si existe el comprobante
    aux = busca_nv(comprobante)
    if aux[0] == 'ok':
        return aux[1]
    else:
        # genero nv
        hoy = datetime.today()
        dir_fecha = str(hoy.year) + '/' + str(hoy.month) + '/' + str(hoy.day)
        directorio = dir_pdf + dir_fecha + '/nv/'
        try:
            os.makedirs(directorio)
        except Exception:
            pass
        genera_nv(fecha, comprobante, pedidonum, items, directorio)


# nota de venta
# fecha
# nro comprobante
# cliente
# item: producto,unitario,cantidad
def genera_nv(fecha, pedidonum, clienteid, items, directorio, nota):
    datos_cliente = obtengo_cliente(clienteid)
    comprobante = 'nv_' + str(pedidonum)
    pdf = FPDF()
    copias = ['ORIGINAL', 'DUPLICADO']

    for i in copias:

        pdf.add_page(orientation='P')

        # recuadro contenedor
        pdf.set_line_width(1.0)
        pdf.rect(15.0, 15.0, 170.0, 245.0)

        # recuadro original-duplicado
        pdf.set_line_width(0.0)
        pdf.rect(15.0, 15.0, 170.0, 10.0)

        # recuadro copia documento
        pdf.set_line_width(0.0)
        pdf.rect(95.0, 25.0, 10.0, 10.0)
        # copia documento
        pdf.set_xy(95.0, 19.0)
        pdf.set_font('arial', 'B', 14.0)
        pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt=i, border=0)

        # letra
        pdf.set_xy(95.0, 29.0)
        pdf.set_font('arial', 'B', 16.0)
        pdf.cell(ln=0, h=3.0, align='C', w=10.0, txt='X', border=0)

        # divisor cabecera
        pdf.set_line_width(0.0)
        pdf.line(100.0, 35.0, 100.0, 57.0)

        # Titulo Documento
        pdf.set_font('arial', '', 16.0)
        pdf.set_xy(115.0, 20.0)
        pdf.cell(ln=0, h=26.0, align='C', w=75.0, txt='Nota de Venta', border=0)

        # bloque datos emisor
        # descomentar para poner imagen
        pdf.image('applications/tapa14/static/images/tapa14-bn-20p.jpg',
                  25.0, 30.0, link='', type='', w=20.0, h=20.0)

        # pdf.set_font('arial', '', 8.0)
        # pdf.set_xy(105.0, 21.0)
        # pdf.cell(ln=0, h=4.0, align='C', w=75.0, txt='Original', border=0)
        # codigo tipo doc
        # pdf.set_font('arial', 'B', 7.0)
        # pdf.set_xy(95.0, 21.5)
        # pdf.cell(ln=0, h=4.5, align='C', w=10.0, txt='COD.00', border=0)

        # numero pedido
        pdf.set_font('arial', 'B', 14.0)
        pdf.set_xy(135.0, 37.5)
        pdf.cell(ln=0, h=9.5, align='L', w=10.0, txt='N\xba', border=0)
        pdf.set_xy(145.0, 37.5)
        pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt=str(pedidonum).zfill(10),
                 border=0)

        # pdf.set_font('arial', 'B', 12.0)
        # pdf.set_xy(17.0, 32.5)
        # pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt=' ', border=0)

        # fecha
        pdf.set_font('arial', '', 12.0)
        pdf.set_xy(135.0, 45.0)
        pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
        pdf.set_xy(155.0, 45.0)
        pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(fecha), border=0)

        # divisor 1 cliente
        # pdf.set_line_width(0.1)
        # pdf.line(15.0, 57.0, 185.0, 57.0)
        # pdf.set_line_width(0.0)
        # pdf.line(15.0, 77.0, 185.0, 77.0)
        # recuadro cliente
        pdf.set_line_width(0.0)
        pdf.rect(15.0, 57.0, 170.0, 20.0)

        # datos cliente
        pdf.set_font('arial', '', 10.0)
        pdf.set_xy(17.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
        pdf.set_xy(35.0, 59.0)
        pdf.cell(ln=0, h=6.0, align='L', w=140.0,
                 txt=str(datos_cliente['razon_social']), border=0)
        pdf.set_xy(17.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Domicilio:', border=0)
        pdf.set_xy(35.0, 64.0)
        pdf.cell(ln=0, h=6.0, align='L', w=125.0,
                 txt=str(datos_cliente['domicilio']), border=0)
        pdf.set_xy(17.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0,
                 txt='Condicion de venta:', border=0)
        pdf.set_xy(55.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=80.0,
                 txt=quito_ce(datos_cliente['tipocuenta']).capitalize(), border=0)
        pdf.set_xy(110.0, 69.0)
        pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
        pdf.set_xy(130.0, 69.0)
        localidad = datos_cliente['localidad']
        provincia = datos_cliente['provincia']
        pdf.cell(ln=0, h=6.0, align='L', w=42.0,
                 txt=str(localidad) + ', ' + str(provincia), border=0)

        # detalle
        # recuadro encabezados
        pdf.set_line_width(0.0)
        pdf.rect(15.0, 77.0, 170.0, 8.0)
        # codigo
        pdf.set_xy(15.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='C\xf3d.', border=0)
        pdf.line(25.0, 77.0, 25.0, 85.0)

        # producto
        pdf.set_xy(26.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Producto', border=0)
        pdf.line(99.0, 77.0, 99.0, 85.0)

        # cantidad
        pdf.set_xy(100.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Cant', border=0)
        pdf.line(111.0, 77.0, 111.0, 85.0)

        # punitario
        pdf.set_xy(112.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='P.Unit', border=0)
        pdf.line(130.0, 77.0, 130.0, 85.0)

        # descuento
        pdf.set_xy(131.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='% Bonif', border=0)
        pdf.line(147.0, 77.0, 147.0, 85.0)

        # subtotal
        pdf.set_xy(160.0, 79.0)
        pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='SubTotal', border=0)

        # pdf.set_xy(36.0, 93.0)
        # pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)

        # items separados 6pts
        # primero pdf.set_xy(36.0, 93.0)
        renglon = 88.0
        col_codigo = 18
        col_producto = 26.0
        col_cant = 101
        col_punit = 113
        col_dto = 132
        col_subt = 153
        paso = 5
        total = 0
        # log(items)
        for i in items:
            subtotal = i['subtotal']
            pdf.set_xy(col_codigo, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=10.0, txt=str(i['codigo']),
                     border=0)
            pdf.set_xy(col_producto, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=60.0, txt=str(i['producto']),
                     border=0)
            pdf.set_xy(col_cant, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=10.0, txt=str(i['cantidad']),
                     border=0)
            pdf.set_xy(col_punit, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=20.0, txt=str(i['preciou']),
                     border=0)
            pdf.set_xy(col_dto, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=20.0,
                     txt=str(i['descuento']),
                     border=0)
            pdf.set_xy(col_subt, renglon)
            pdf.cell(ln=0, h=4.0, align='R', w=30.0, txt=str(subtotal),
                     border=0)
            renglon += paso
            total += subtotal

        # nota
        if str(nota) != '':
            renglon += paso
            pdf.set_xy(col_producto, renglon)
            pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Nota: ' + str(nota),
                     border=0)

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

    documento = directorio + str(comprobante) + '.pdf'
    pdf.output(documento, 'F')
    log('documento en: ' + str(documento))
    return documento


def genera_nv1(fecha, pedidonum, clienteid, items, directorio, nota):
    datos_cliente = obtengo_cliente(clienteid)
    comprobante = 'nv_' + str(pedidonum)
    pdf = FPDF()
    pdf.add_page(orientation='P')
    # hoja1
    offset = 0
    copia = "ORIGINAL"
    # recuadro contenedor
    pdf.set_line_width(1.0)
    pdf.rect(25.0, offset + 15.0, 170.0, 125.0)
    # recuadro original-duplicado
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 15.0, 170.0, 10.0)

    # recuadro copia documento
    pdf.set_line_width(0.0)
    pdf.rect(105.0, offset + 25.0, 10.0, 10.0)
    # copia documento
    pdf.set_xy(105.0, offset + 19.0)
    pdf.set_font('arial', 'B', 14.0)
    pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt=str(copia), border=0)

    # letra
    pdf.set_xy(105.0, offset + 29.0)
    pdf.set_font('arial', 'B', 16.0)
    pdf.cell(ln=0, h=3.0, align='C', w=10.0, txt='X', border=0)

    # divisor cabecera
    pdf.set_line_width(0.0)
    pdf.line(110.0, offset + 35.0, 110.0, offset + 53.0)

    # Titulo Documento
    pdf.set_font('arial', '', 16.0)
    pdf.set_xy(125.0, offset + 18.0)
    pdf.cell(ln=0, h=26.0, align='C', w=75.0, txt='Nota de Venta', border=0)

    # bloque datos emisor
    # descomentar para poner imagen
    pdf.image('applications/tapa14/static/images/tapa14-bn-20p.jpg',
              20.0, 30.0, link='', type='', w=20.0, h=20.0)

    # numero pedido
    pdf.set_font('arial', 'B', 14.0)
    pdf.set_xy(134.0, offset + 35)
    pdf.cell(ln=0, h=9.5, align='L', w=10.0, txt='N\xba', border=0)
    pdf.set_xy(142.0, offset + 35)
    pdf.cell(ln=0, h=9.5, align='L', w=60.0,
             txt=str(pedidonum).zfill(10), border=0)

    # fecha
    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(134.0, offset + 43.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
    pdf.set_xy(154.0, offset + 43.0)
    pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(fecha), border=0)

    # recuadro cliente
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 53.0, 170.0, 20.0)

    # datos cliente
    pdf.set_font('arial', '', 10.0)
    pdf.set_xy(27.0, offset + 55.0)
    pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
    pdf.set_xy(45.0, offset + 55.0)
    pdf.cell(ln=0, h=6.0, align='L', w=140.0,
             txt=str(datos_cliente['razon_social']), border=0)
    pdf.set_xy(27.0, offset + 60.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Domicilio:', border=0)
    pdf.set_xy(45.0, offset + 60.0)
    pdf.cell(ln=0, h=6.0, align='L', w=125.0,
             txt=str(datos_cliente['domicilio']), border=0)
    pdf.set_xy(27.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0,
             txt='Condicion de venta:', border=0)
    pdf.set_xy(65.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=80.0,
             txt=quito_ce(datos_cliente['tipocuenta']).capitalize(), border=0)
    pdf.set_xy(120.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
    pdf.set_xy(140.0, offset + 65.0)
    localidad = datos_cliente['localidad']
    provincia = datos_cliente['provincia']
    pdf.cell(ln=0, h=6.0, align='L', w=42.0,
             txt=str(localidad) + ', ' + str(provincia), border=0)

    # detalle
    col_codigo = 27
    col_producto = 46.0
    col_cant = 118
    col_punit = 138
    col_subt = 163

    # recuadro encabezados
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 73.0, 170.0, 8.0)
    # codigo
    pdf.set_xy(col_codigo, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='C\xf3digo', border=0)
    pdf.line(col_codigo + 17, offset + 73.0, col_codigo + 17, offset + 81.0)

    # producto
    pdf.set_xy(col_producto, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Producto', border=0)
    pdf.line(col_producto + 70, offset + 73.0,
             col_producto + 70, offset + 81.0)

    # cantidad
    pdf.set_xy(col_cant, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Cantidad', border=0)
    pdf.line(col_cant + 18, offset + 73.0, col_cant + 18, offset + 81.0)

    # punitario
    pdf.set_xy(col_punit, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='R', w=25.0, txt='Precio Unitario', border=0)
    pdf.line(col_punit + 28, offset + 73.0, col_punit + 28, offset + 81.0)

    # subtotal
    pdf.set_xy(col_subt, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='R', w=28.0, txt='SubTotal', border=0)

    # nota
    renglon = 84
    ult_renglon = offset + 130
    pdf.set_xy(col_producto, offset + renglon)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)
    renglon = renglon + 6

    # pdf.set_xy(36.0, 93.0)
    # pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)

    # items separados 6pts
    # primero pdf.set_xy(36.0, 93.0)

    paso = 5
    total = 0
    # log(items)
    for i in items:
        parcial = i[0][0] * i[0][2]
        pdf.set_xy(col_producto, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='L', w=60.0, txt=str(i[0][1]), border=0)
        pdf.set_xy(col_cant, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=10.0, txt=str(i[0][0]), border=0)
        pdf.set_xy(col_punit, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=20.0, txt=str(i[0][2]), border=0)
        pdf.set_xy(col_subt, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=30.0, txt=str(parcial), border=0)
        renglon = renglon + paso
        total = total + parcial

    pdf.set_line_width(0.0)
    pdf.line(25.0, offset + 127.0, 195.0, offset + 127.0)

    pdf.set_font('arial', 'B', 12.0)
    pdf.set_xy(col_subt, ult_renglon)
    pdf.cell(ln=0, h=9.0, align='R', w=30.0, txt=str(total), border=1)
    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(col_punit, ult_renglon)
    pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)

    # divisor
    pdf.set_line_width(0.0)
    pdf.line(5, 146, 205.0, 146)

    # hoja2

    offset = 135
    copia = "DUPLICADO"
    # recuadro contenedor
    pdf.set_line_width(1.0)
    pdf.rect(25.0, offset + 15.0, 170.0, 125.0)
    # recuadro original-duplicado
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 15.0, 170.0, 10.0)

    # recuadro copia documento
    pdf.set_line_width(0.0)
    pdf.rect(105.0, offset + 25.0, 10.0, 10.0)
    # copia documento
    pdf.set_xy(105.0, offset + 19.0)
    pdf.set_font('arial', 'B', 14.0)
    pdf.cell(ln=0, h=2.0, align='C', w=10.0, txt=str(copia), border=0)

    # letra
    pdf.set_xy(105.0, offset + 29.0)
    pdf.set_font('arial', 'B', 16.0)
    pdf.cell(ln=0, h=3.0, align='C', w=10.0, txt='X', border=0)

    # divisor cabecera
    pdf.set_line_width(0.0)
    pdf.line(110.0, offset + 35.0, 110.0, offset + 53.0)

    # Titulo Documento
    pdf.set_font('arial', '', 16.0)
    pdf.set_xy(125.0, offset + 18.0)
    pdf.cell(ln=0, h=26.0, align='C', w=75.0, txt='Nota de Venta', border=0)

    # bloque datos emisor
    # descomentar para poner imagen
    pdf.image('applications/tapa14/static/images/tapa14-bn-20p.jpg',
              20.0, 30.0, link='', type='', w=20.0, h=20.0)

    # numero pedido
    pdf.set_font('arial', 'B', 14.0)
    pdf.set_xy(134.0, offset + 35)
    pdf.cell(ln=0, h=9.5, align='L', w=10.0, txt='N\xba', border=0)
    pdf.set_xy(142.0, offset + 35)
    pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt=str(pedidonum).zfill(10),
             border=0)

    # fecha
    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(134.0, offset + 43.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Fecha:', border=0)
    pdf.set_xy(154.0, offset + 43.0)
    pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=str(fecha), border=0)

    # recuadro cliente
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 53.0, 170.0, 20.0)

    # datos cliente
    pdf.set_font('arial', '', 10.0)
    pdf.set_xy(27.0, offset + 55.0)
    pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Sr.(s):', border=0)
    pdf.set_xy(45.0, offset + 55.0)
    pdf.cell(ln=0, h=6.0, align='L', w=140.0,
             txt=str(datos_cliente['razon_social']), border=0)
    pdf.set_xy(27.0, offset + 60.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0,
             txt='Domicilio:', border=0)
    pdf.set_xy(45.0, offset + 60.0)
    pdf.cell(ln=0, h=6.0, align='L', w=125.0,
             txt=str(datos_cliente['domicilio']), border=0)
    pdf.set_xy(27.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0,
             txt='Condicion de venta:', border=0)
    pdf.set_xy(65.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=80.0,
             txt=quito_ce(datos_cliente['tipocuenta']).capitalize(), border=0)
    pdf.set_xy(120.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Localidad:', border=0)
    pdf.set_xy(140.0, offset + 65.0)
    pdf.cell(ln=0, h=6.0, align='L', w=42.0,
             txt=str(localidad) + ', ' + str(provincia), border=0)

    # detalle
    col_codigo = 27
    col_producto = 46.0
    col_cant = 118
    col_punit = 138
    col_subt = 163

    # recuadro encabezados
    pdf.set_line_width(0.0)
    pdf.rect(25.0, offset + 73.0, 170.0, 8.0)
    # codigo
    pdf.set_xy(col_codigo, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='C\xf3digo', border=0)
    pdf.line(col_codigo + 17, offset + 73.0, col_codigo + 17, offset + 81.0)

    # producto
    pdf.set_xy(col_producto, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Producto', border=0)
    pdf.line(col_producto + 70, offset + 73.0,
             col_producto + 70, offset + 81.0)

    # cantidad
    pdf.set_xy(col_cant, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt='Cantidad', border=0)
    pdf.line(col_cant + 18, offset + 73.0, col_cant + 18, offset + 81.0)

    # punitario
    pdf.set_xy(col_punit, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='R', w=25.0, txt='Precio Unitario', border=0)
    pdf.line(col_punit + 28, offset + 73.0, col_punit + 28, offset + 81.0)

    # subtotal
    pdf.set_xy(col_subt, offset + 75.0)
    pdf.cell(ln=0, h=4.0, align='R', w=28.0, txt='SubTotal', border=0)

    # nota
    renglon = 84
    ult_renglon = offset + 130
    pdf.set_xy(col_producto, offset + renglon)
    pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)
    renglon = renglon + 6

    # pdf.set_xy(36.0, 93.0)
    # pdf.cell(ln=0, h=4.0, align='L', w=125.0, txt=str(nota), border=0)

    # items separados 6pts
    # primero pdf.set_xy(36.0, 93.0)

    paso = 5
    total = 0
    # log(items)
    for i in items:
        parcial = i[0][0] * i[0][2]
        pdf.set_xy(col_producto, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='L', w=60.0, txt=str(i[0][1]), border=0)
        pdf.set_xy(col_cant, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=10.0, txt=str(i[0][0]), border=0)
        pdf.set_xy(col_punit, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=20.0, txt=str(i[0][2]), border=0)
        pdf.set_xy(col_subt, offset + renglon)
        pdf.cell(ln=0, h=4.0, align='R', w=30.0, txt=str(parcial), border=0)
        renglon = renglon + paso
        total = total + parcial

    pdf.set_line_width(0.0)
    pdf.line(25.0, offset + 127.0, 195.0, offset + 127.0)

    pdf.set_font('arial', 'B', 12.0)
    pdf.set_xy(col_subt, ult_renglon)
    pdf.cell(ln=0, h=9.0, align='R', w=30.0, txt=str(total), border=1)
    pdf.set_font('arial', '', 12.0)
    pdf.set_xy(col_punit, ult_renglon)
    pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)

    documento = directorio + str(comprobante) + '.pdf'
    pdf.output(documento, 'F')
    log('documento en: ' + str(documento))
    return documento


def test_genera_nv():
    pedidonum = 19
    test = obtengo_pedido(pedidonum)
    if test['fentrega'] is None:
        fecha = '19/6/2018'
    else:
        fecha = (str(test[1].day) + '/' + str(test[1].month) + '/' +
                 str(test[1].year))
    clienteid = test['cliente_id']
    log(clienteid)
    nota = test['nota']
    items = test['productos']
    # directorio='applications/dev/pdf/2018/6/19/nv/'
    directorio = files_dir + 'pdf/test/nv/'
    try:
        os.makedirs(directorio)
    except Exception:
        pass
    return genera_nv(fecha, pedidonum, clienteid, items, directorio, nota)


def quito_ce(palabra):
    caracteres_permitidos = ('0123456789' +
                             'abcdefghijklmnopqrstuvwxyz' +
                             'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    allowed_chars = set(caracteres_permitidos)
    if palabra is None:
        return 'error'
    resultado = ''
    for i in palabra:
        if i in allowed_chars:
            resultado = resultado + i
    return resultado
