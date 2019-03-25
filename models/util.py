#websocket
#from gluon.contrib.websocket_messaging import websocket_send

#estructura tree
from collections import defaultdict

def tree():
    return defaultdict(tree)


#logger
import logging
logger = logging.getLogger("web2py")
logger.setLevel(logging.DEBUG)
log_remove = [
	'Set-Cookie: ',
	'session_id_tapa14=']

def log(palabra):
    """funcion auxiliar de auditoria que incorpora el usuario si es que existe"""
    if hasattr(auth.user, 'email'):
        #mensaje=str(auth.user.email)+' '+str(request.cookies)+' '+str(request.function)+' '+str(palabra)
        mensaje=str(auth.user.email)+' '+str(request.function)+' '+str(palabra)
        for i in log_remove:
            mensaje = mensaje.replace(str(i),'')
        logger.info(mensaje)
    else:
        logger.info('usuario: admin '+str(palabra))
  
def debug(palabra):
    if hasattr(auth.user, 'email'):
        mensaje='DEBUG-'+str(palabra)+'-FIN'
        for i in log_remove:
             mensaje = mensaje.replace(str(i),'')
        logger.info(mensaje)
    else:
         logger.info('usuario: admin '+str(palabra))