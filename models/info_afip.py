# -*- coding: utf-8 -*-

# de utils.py de https://github.com/reingart/pyafipws
# Tipos de datos (código RG1361)

# cambio por tipodato - compatibilidad web2py A()
# N = 'Numerico'      # 2
# A = 'Alfanumerico'  # 3
# I = 'Importe'       # 4
# C = A               # 1 (caracter alfabetico)
# B = A               # 9 (blanco)

tipodato = {
    'N': 'Numerico',
    'A': 'Alfanumerico',
    'I': 'Importe',
    'C': 'Alfanumerico',
    'B': 'Alfanumerico',
}

# de sired.py de https://github.com/reingart/pyafipws
# Diseño de registro de Importación de comprobantes de Ventas

categorias = {"responsable inscripto": "01",  # IVA Responsable Inscripto
              "responsable no inscripto": "02",  # IVA Responsable no Inscripto
              "no responsable": "03",  # IVA no Responsable
              "exento": "04",  # IVA Sujeto Exento
              "consumidor final": "05",  # Consumidor Final
              "monotributo": "06",  # Responsable Monotributo
              "responsable monotributo": "06",  # Responsable Monotributo
              "no categorizado": "07",  # Sujeto no Categorizado
              "importador": "08",  # Importador del Exterior
              "exterior": "09",  # Cliente del Exterior
              "liberado": "10",  # IVA Liberado Ley Nº 19.640
              "responsable inscripto - agente de percepción": "11",
              # IVA Responsable Inscripto - Agente de Percepcion
              }

codigos_operacion = {
    "Z": "Exportaciones a la zona franca",
    "X": "Exportaciones al Exterior",
    "E": "Operaciones Exentas",
}

CAB_FAC_TIPO1 = [ # 
    ('tipo_reg', 1, tipodato['N']),
    ('fecha_cbte', 8, tipodato['N']),
    ('tipo_cbte', 2, tipodato['N']),
    ('ctl_fiscal', 1, tipodato['C']),
    ('punto_vta', 4, tipodato['N']),
    ('cbt_numero', 8, tipodato['N']),
    ('cbte_nro_reg', 8, tipodato['N']),
    ('cant_hojas', 3, tipodato['N']),
    ('tipo_doc', 2, tipodato['N']),
    ('nro_doc', 11, tipodato['N']),
    ('nombre', 30, tipodato['A']),
    ('imp_total', 15, tipodato['I']),
    ('imp_tot_conc', 15, tipodato['I']),
    ('imp_neto', 15, tipodato['I']),
    ('impto_liq', 15, tipodato['I']),
    ('impto_liq_rni', 15, tipodato['I']),
    ('imp_op_ex', 15, tipodato['I']),
    ('impto_perc', 15, tipodato['I']),
    ('imp_iibb', 15, tipodato['I']),
    ('impto_perc_mun', 15, tipodato['I']),
    ('imp_internos', 15, tipodato['I']),
    ('transporte', 15, tipodato['I']),
    ('categoria', 2, tipodato['N']),
    ('imp_moneda_id', 3, tipodato['A']),
    ('imp_moneda_ctz', 10, tipodato['I']),
    ('alicuotas_iva', 1, tipodato['N']),
    ('codigo_operacion', 1, tipodato['C']),
    ('cae', 14, tipodato['N']),
    ('fecha_vto', 8, tipodato['N']),
    ('fecha_anulacion', 8, tipodato['A']),
]

# campos especiales del encabezado:
IMPORTES = ('imp_total', 'imp_tot_conc', 'imp_neto', 'impto_liq',
            'impto_liq_rni', 'imp_op_ex', 'impto_perc', 'imp_iibb',
            'impto_perc_mun', 'imp_internos')

# total
CAB_FAC_TIPO2 = [
    ('tipo_reg', 1, tipodato['N']),
    ('periodo', 6, tipodato['N']),
    ('relleno', 13, tipodato['B']),
    ('cant_reg_tipo_1', 8, tipodato['N']),
    ('relleno', 17, tipodato['B']),
    ('cuit', 11, tipodato['N']),
    ('relleno', 22, tipodato['B']),
    ('imp_total', 15, tipodato['I']),
    ('imp_tot_conc', 15, tipodato['I']),
    ('imp_neto', 15, tipodato['I']),
    ('impto_liq', 15, tipodato['I']),
    ('impto_liq_rni', 15, tipodato['I']),
    ('imp_op_ex', 15, tipodato['I']),
    ('impto_perc', 15, tipodato['I']),
    ('imp_iibb', 15, tipodato['I']),
    ('impto_perc_mun', 15, tipodato['I']),
    ('imp_internos', 15, tipodato['I']),
    ('relleno', 62, tipodato['B']),
]

DETALLE = [
    ('tipo_cbte', 2, tipodato['N']),
    ('ctl_fiscal', 1, tipodato['C']),
    ('fecha_cbte', 8, tipodato['N']),
    ('punto_vta', 4, tipodato['N']),
    ('cbt_numero', 8, tipodato['N']),
    ('cbte_nro_reg', 8, tipodato['N']),
    ('qty', 12, tipodato['I']),
    ('pro_umed', 2, tipodato['N']),
    ('pro_precio_uni', 16, tipodato['I']),
    ('imp_bonif', 15, tipodato['I']),
    ('imp_ajuste', 16, tipodato['I']),
    ('imp_total', 16, tipodato['I']),
    ('alicuota_iva', 4, tipodato['I']),
    ('gravado', 1, tipodato['C']),
    ('anulacion', 1, tipodato['C']),
    ('codigo', 50, tipodato['A']),
    ('ds', 150, tipodato['A']),
]

VENTAS_TIPO1 = [
    ('tipo_reg', 1, tipodato['N']),
    ('fecha_cbte', 8, tipodato['N']),
    ('tipo_cbte', 2, tipodato['N']),
    ('ctl_fiscal', 1, tipodato['C']),
    ('punto_vta', 4, tipodato['N']),
    ('cbt_numero', 20, tipodato['N']),
    ('cbte_nro_reg', 20, tipodato['N']),
    ('tipo_doc', 2, tipodato['N']),
    ('nro_doc', 11, tipodato['N']),
    ('nombre', 30, tipodato['A']),
    ('imp_total', 15, tipodato['I']),
    ('imp_tot_conc', 15, tipodato['I']),
    ('imp_neto', 15, tipodato['I']),
    ('alicuota_iva', 4, tipodato['I']),
    ('impto_liq', 15, tipodato['I']),
    ('impto_liq_rni', 15, tipodato['I']),
    ('imp_op_ex', 15, tipodato['I']),
    ('impto_perc', 15, tipodato['I']),
    ('imp_iibb', 15, tipodato['I']),
    ('impto_perc_mun', 15, tipodato['I']),
    ('imp_internos', 15, tipodato['I']),
    ('categoria', 2, tipodato['N']),
    ('imp_moneda_id', 3, tipodato['A']),
    ('imp_moneda_ctz', 10, tipodato['I']),
    ('alicuotas_iva', 1, tipodato['N']),
    ('codigo_operacion', 1, tipodato['C']),
    ('cae', 14, tipodato['N']),
    ('fecha_vto', 8, tipodato['N']),
    ('fecha_anulacion', 8, tipodato['A']),
    ('info_adic', 75 - 0, tipodato['B']),
]

VENTAS_TIPO2 = [
    ('tipo_reg', 1, tipodato['N']),
    ('periodo', 6, tipodato['N']),
    ('relleno', 29, tipodato['B']),
    ('cant_reg_tipo_1', 12, tipodato['N']),
    ('relleno', 10, tipodato['B']),
    ('cuit', 11, tipodato['N']),
    ('relleno', 30, tipodato['B']),
    ('imp_total', 15, tipodato['I']),
    ('imp_tot_conc', 15, tipodato['I']),
    ('imp_neto', 15, tipodato['I']),
    ('Relleno', 4, tipodato['B']),
    ('impto_liq', 15, tipodato['I']),
    ('impto_liq_rni', 15, tipodato['I']),
    ('imp_op_ex', 15, tipodato['I']),
    ('impto_perc', 15, tipodato['I']),
    ('imp_iibb', 15, tipodato['I']),
    ('impto_perc_mun', 15, tipodato['I']),
    ('imp_internos', 15, tipodato['I']),
    ('relleno', 122, tipodato['B']),
]

# de rg3685.py de https://github.com/reingart/pyafipws

# Diseño de registro de Importación de comprobantes de Ventas

REGINFO_CV_VENTAS_CBTE = [
    ('fecha_cbte', 8, tipodato['N']),
    ('tipo_cbte', 2, tipodato['N']),
    ('punto_vta', 5, tipodato['N']),
    ('cbt_desde', 20, tipodato['N']),
    ('cbt_hasta', 20, tipodato['N']),
    ('tipo_doc', 2, tipodato['N']),
    ('nro_doc', 20, tipodato['N']),
    ('nombre', 30, tipodato['A']),
    ('imp_total', 15, tipodato['I']),
    ('imp_tot_conc', 15, tipodato['I']),
    ('impto_liq_rni', 15, tipodato['I']),
    ('imp_op_ex', 15, tipodato['I']),
    ('impto_perc', 15, tipodato['I']),
    ('imp_iibb', 15, tipodato['I']),
    ('impto_perc_mun', 15, tipodato['I']),
    ('imp_internos', 15, tipodato['I']),
    ('moneda_id', 3, tipodato['A']),
    ('moneda_ctz', 10, tipodato['I'], 6),
    ('cant_alicuota_iva', 1, tipodato['N']),
    ('codigo_operacion', 1, tipodato['C']),
    ('imp_trib', 15, tipodato['I']),
    ('fecha_venc_pago', 8, tipodato['A']),
]

# Diseño de registro de Importación de Alícuotas de comprobantes de Ventas

REGINFO_CV_VENTAS_CBTE_ALICUOTA = [
    ('tipo_cbte', 3, tipodato['N']),
    ('punto_vta', 5, tipodato['N']),
    ('cbt_numero', 20, tipodato['N']),
    ('base_imp', 15, tipodato['I']),
    ('iva_id', 4, tipodato['N']),
    ('importe', 15, tipodato['I']),
]
