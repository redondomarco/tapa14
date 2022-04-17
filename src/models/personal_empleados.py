# -*- coding: utf-8 -*-

import datetime
from collections import defaultdict
# for ide
if 1 == 2:
    from gluon import Field, auth
    from gluon.validators import IS_IN_SET
    from db import db
    from log import log
    from personal_fuente_datos import marcadas_tunel_latix
    from util import datetime_sp, ssh_command, s_horario

dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves',
               'Viernes', 'Sabado']

db.define_table(
    'marcadas',
    Field('id_reg'),
    Field('user_code'),
    Field('datetime'),
    Field('bkp_type'),
    Field('type_code'),
    Field('huella', unique=True, length=40)
)

db.define_table(
    'empleado',
    Field('nombre', length=255),
    Field('apellido', length=255),
    Field('user_code', 'integer', unique=True, length=4),
    Field('dias'),
    Field('entrada', 'time'),
    Field('salida', 'time'),
    Field('descanso', 'time'),
    auth.signature,
    format='%(nombre)s %(apellido)s',
)
db.empleado.dias.requires = IS_IN_SET(dias_semana, multiple=True)


def huella(id_reg, user_code, datetime, bkp_type, type_code):
    salida = (str(id_reg) +
              str(user_code) +
              str(datetime.isoformat()) +
              str(bkp_type) +
              str(type_code))
    return salida


# actualizo marcadas
def actualizo_marcadas():
    try:
        log('activo reloj con ping')
        ssh_command('pegasus',
                    'ping -c 4 192.168.0.45')
        log('descargo todas las marcadas en pegasus')
        ssh_command('pegasus',
                    'cd /root/anviz/anviz-sync && anviz-sync --all')
        log('descarga finalizada')
        marcadas = marcadas_tunel_latix()
        if marcadas[0] == 'ok':
            for registro in marcadas[1]:
                huellagen = huella(registro[0], registro[1], registro[2],
                                   registro[3], registro[4])
                marcada = {'id_reg': registro[0],
                           'user_code': registro[1],
                           'datetime': registro[2],
                           'bkp_type': registro[3],
                           'type_code': registro[4],
                           'huella': huellagen}
                if db(db.marcadas.huella == huellagen).select().first():
                    pass
                else:
                    db['marcadas'].insert(**marcada)
            db.commit()
            mensaje = ['ok', 'proceso exitoso']
    except Exception as e:
        mensaje = ['error', str(e)]
    log(mensaje)
    return mensaje


def test_planilla():
    user_code = 1001
    fdesde = '2020-02-1'
    fhasta = '2020-02-20'
    tdesde = datetime.datetime.strptime(fdesde, '%Y-%m-%d')
    thasta = datetime.datetime.strptime(fhasta, '%Y-%m-%d')
    print(f"{tdesde} {thasta}")
    marcadas = db((db.marcadas.datetime >= tdesde) &
                  (db.marcadas.datetime <= thasta) &
                  (db.marcadas.user_code == user_code)).select()
    return marcadas


def marcadas_usuario_fechas(user_code, fdesde, fhasta):
    tdesde = datetime.datetime.strptime(fdesde, '%Y-%m-%d')
    # fhasta es hasta las 23:59 del dia
    thasta = (datetime.datetime.strptime(fhasta, '%Y-%m-%d') +
              datetime.timedelta(seconds=86340))
    marcadas = db((db.marcadas.datetime >= tdesde) &
                  (db.marcadas.datetime <= thasta) &
                  (db.marcadas.user_code == user_code)).select()
    return marcadas.as_dict()


def test_marcadas_usuario_fechas():
    user_code = 1018
    fdesde = '2021-02-22'
    fhasta = '2021-02-23'
    return marcadas_usuario_fechas(user_code, fdesde, fhasta)


def proceso_dias(marcadas_dict):
    # separo en dias
    dias_t = defaultdict(list)
    for i in marcadas_dict.keys():
        s_fechadia = marcadas_dict[i]['datetime']
        fechadia = datetime.datetime.strptime(s_fechadia, '%Y-%m-%d %H:%M:%S')
        dias_t[fechadia.day].append(fechadia)
    return dias_t


def test_proceso_marcadas():
    marcadas_dict = test_marcadas_usuario_fechas()
    return proceso_dias(marcadas_dict)


def proceso_horarios(horarios_list):
    "ordeno una lista de horarios y devuelvo el menor y el mayor"
    horarios_list.sort()
    return [horarios_list[0], horarios_list[-1]]


def test_proceso_horarios():
    horarios_list = [datetime.time(5, 31, 18),
                     datetime.time(5, 36, 43),
                     datetime.time(14, 19, 56),
                     datetime.time(13, 49, 56)]
    return proceso_horarios(horarios_list)


def aplico_politica(user_code, fdesde, fhasta):
    # obtengo marcadas
    marcadas = marcadas_usuario_fechas(user_code, fdesde, fhasta)
    dias_t = proceso_dias(marcadas)
    tabla = []
    for dia in dias_t.keys():
        horario = proceso_horarios(dias_t[dia])
        show_horario = s_horario(horario)
        td = horario[1] - horario[0]
        # days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        minutos = str(minutes).zfill(2)
        tabla.append({'dia': dia,
                      'horario': show_horario,
                      'horas': f'{hours}:{minutos}'})
    return tabla


def sumo_horas(tabla):
    suma = datetime.timedelta(seconds=0)
    for fila in tabla:
        log(f'valor fila: {fila}')
        tiempo = fila['horas'].split(':')
        log(tiempo)
        suma = suma + datetime.timedelta(
            hours=int(tiempo[0]),
            minutes=int(tiempo[1]))
    secs = suma.total_seconds()
    hours = int(secs / 3600)
    secs = secs - (hours * 3600)
    minutes = int(secs / 60)
    log(f'calculo suma: {hours} horas {minutes} minutos')
    return (f'{hours} horas y {minutes} minutos')


def test_aplico_politica():
    user_code = 1001
    fdesde = '2020-02-1'
    fhasta = '2020-02-29'
    return aplico_politica(user_code, fdesde, fhasta)
