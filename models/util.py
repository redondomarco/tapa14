import logging
from collections import defaultdict
import hashlib


# for ide
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

# logs
logger = logging.getLogger("web2py")
logger.setLevel(logging.DEBUG)
log_remove = [
    'Set-Cookie: ',
    'session_id_tapa14=']


def log(palabra):
    """funcion auditoria que incorpora el usuario si es que existe"""
    if hasattr(auth.user, 'email'):
        mensaje = (str(auth.user.email) + ' '
        + str(request.function) + ' ' + str(palabra))
        for i in log_remove:
            mensaje = mensaje.replace(str(i), '')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin ' + str(palabra))


def debug(palabra):
    if hasattr(auth.user, 'email'):
        mensaje = 'DEBUG-' + str(palabra) + '-FIN'
        for i in log_remove:
            mensaje = mensaje.replace(str(i), '')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin ' + str(palabra))

# websocket
# from gluon.contrib.websocket_messaging import websocket_send


def tree():
    return defaultdict(tree)


# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def md5sum(filepath):
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
