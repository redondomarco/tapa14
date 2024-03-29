# -*- coding: utf-8 -*-

import logging

# for ide
if 1 == 2:
    from gluon import request, auth

# logs
logger = logging.getLogger("w2p.tapa14")
logger.setLevel(logging.DEBUG)
log_remove = [
    'Set-Cookie: ',
    'session_id_tapa14=']


def log(palabra):
    """funcion auditoria que incorpora el usuario si es que existe"""
    if hasattr(auth.user, 'email'):
        ipclient = str(request.client)
        usuario = str(auth.user.email)
        function = str(request.function)
        palabra = str(palabra)
        mensaje = f"{usuario} {ipclient} {function} {palabra}"
        for i in log_remove:
            mensaje = mensaje.replace(str(i), '')
    else:
        mensaje = f'usuario: admin {palabra}'
    logger.info(mensaje)
