# -*- coding: utf-8 -*-

import psycopg2
from sshtunnel import SSHTunnelForwarder

# for ide
if False:
    from db import configuration


# For interactive work (on ipython) it's easier to work with explicit objects
# instead of contexts.
# Create an SSH tunnel
def marcadas_tunel_latix():
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
    return result

# en appconfig.ini
# [datos]
# ssh_host =
# ssh_port =
# ssh_user =
# ssh_pass =
# db_name =
# db_user =
# db_pass =
