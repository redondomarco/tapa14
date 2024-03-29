# -*- coding: utf-8 -*-

import imp
import psycopg2
import time
from sshtunnel import SSHTunnelForwarder

# for ide
if 1 == 2:
    from db import configuration
    from log import log
    from info_afip import tipodato


# For interactive work (on ipython) it's easier to work with explicit objects
# instead of contexts.
# Create an SSH tunnel
def marcadas_tunel_latix():
    try:
        log('inicio descarga')
        tunnel = SSHTunnelForwarder(
            (configuration.get('datos.ssh_host'),
             configuration.get('datos.ssh_port')),
            ssh_username=configuration.get('datos.ssh_user'),
            ssh_password=configuration.get('datos.ssh_pass'),
            remote_bind_address=('localhost', 5432),
            local_bind_address=('localhost', 6543))
        # Start the tunnel
        tunnel.start()
        # Create a database connection
        conn = psycopg2.connect(
            database=configuration.get('datos.db_name'),
            user=configuration.get('datos.db_user'),
            password=configuration.get('datos.db_pass'),
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port,
        )
        # Get a database cursor
        cur = conn.cursor()
        # Execute SQL
        cur.execute("""select * from attendance_record;""")
        # Get the result
        result = cur.fetchall()
        # Close connections
        conn.close()
        # Stop the tunnel
        tunnel.stop()
        if tunnel.is_alive:
            time.sleep(1)
            log('reintentando cerrar tunnel')
            tunnel.close()
        log(f'actualizo marcadas: ok')
        mensaje = ['ok', result]
    except Exception as e:
        mensaje = ['error', str(e)]
        log(f'actualizo marcadas: {mensaje}')
    return mensaje

# en appconfig.ini
# [datos]
# ssh_host =
# ssh_port =
# ssh_user =
# ssh_pass =
# db_name =
# db_user =
# db_pass =
