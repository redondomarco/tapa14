# -*- coding: utf-8 -*-
from decimal import Decimal

# for ide
if 1 == 2:
    from log import log
    import datetime
    from info_afip import tipodato


# de utils.py https://github.com/reingart/pyafipws

def leer(linea, formato, expandir_fechas=False):
    "Analiza una linea de texto dado un formato, devuelve un diccionario"
    dic = {}
    comienzo = 1
    for fmt in formato:
        clave, longitud, tipo = fmt[0:3]
        dec = (len(fmt) > 3 and isinstance(fmt[3], int)) and fmt[3] or 2
        valor = linea[comienzo - 1:comienzo - 1 + longitud].strip()
        try:
            # log('debug: '+ str(fmt[0]) + ':' + valor)
            if chr(8) in valor or chr(127) in valor or chr(255) in valor:
                valor = None        # nulo
            elif tipo == tipodato['N']:
                if valor:
                    valor = int(valor)
                else:
                    valor = 0
                if clave.lower().startswith("fec"):
                    valor = datetime.datetime.strptime(str(valor), '%Y%m%d')
            elif tipo == tipodato['I']:
                if valor:
                    try:
                        if '.' in valor:
                                valor = float(valor)
                        else:
                            valor = valor.strip(" ")
                            if valor[0] == "-":
                                sign = -1
                                valor = valor[1:]
                            else:
                                sign = +1
                            valor = sign * float(
                                ("%%s.%%0%sd" % dec) % (
                                    int(valor[:-dec] or
                                        '0'), int(valor[-dec:] or '0')))
                            valor = Decimal(valor)
                    except ValueError:
                        raise ValueError("Campo invalido: %s = '%s'" % (
                            clave, valor))
                else:
                    valor = Decimal(0.00)
            elif (clave.lower().startswith("fec") and longitud <= 8):
                if valor:
                    if valor == '00000000':
                        valor = None
                    else:
                        log('aaa')
                        valor = datetime.datetime.strptime(str(valor), '%Y%m%d')
                    # valor = "%s-%s-%s" % (valor[0:4], valor[4:6], valor[6:8])
                else:
                    valor = None
            else:
                # valor = valor.decode("ascii", "ignore")
                # log('debug-' + valor + '-')
                pass
            if not valor and clave in dic and len(linea) <= comienzo:
                pass    # ignorar - compatibilidad hacia atrás (cambios tamaño)
            else:
                dic[clave] = valor
            comienzo += longitud
        except Exception as e:
            raise ValueError("Error al leer campo %s pos %s val '%s': %s" % (
                clave, comienzo, valor, str(e)))
    return dic
