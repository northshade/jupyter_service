import os

c = get_config()
pwd = os.path.dirname(__file__)

c.JupyterHub.spawner_class = 'cassinyspawner.SwarmSpawner'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.base_url = '/dag'

c.JupyterHub.cleanup_servers = True

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 5

c.SwarmSpawner.jupyterhub_service_name = 'nbibda_service_jupyterhub'

c.SwarmSpawner.networks = ["nbibda_service_default"]

notebook_dir = os.environ.get('NOTEBOOK_DIR') or '/home/jovyan/work/'
c.SwarmSpawner.notebook_dir = notebook_dir

mounts = [{'type': 'volume',
           'driver_config': 'rasmunk/sshfs:next',
           'driver_options': {'sshcmd': '{sshcmd}', 'id_rsa': '{id_rsa}',
                              'allow_other': '', 'big_writes': '',
                              'reconnect': ''},
           'source': 'sshvolume-user-{username}',
           'target': notebook_dir
           }]

# 'args' is the command to run inside the service
c.SwarmSpawner.container_spec = {
    'args': ['/usr/local/bin/start-singleuser.sh'],
    # image needs to be previously pulled
    'Image': '127.0.0.1:5000/nbi_jupyter_notebook',
    'mounts': mounts
}

# Available docker images the user can spawn
c.SwarmSpawner.dockerimages = [
    {'image': '127.0.0.1:5000/nbi_jupyter_notebook',
     'name': 'Image with default MiG Homedrive mount, supports Py2/3 and R'}
]

# Authenticator -> remote user header
c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator' \
                                   '.remote_user_auth' \
                                   '.MIGMountRemoteUserAuthenticator'

# Limit cpu/mem to 4 cores/8 GB mem
# During conjestion, kill random internal processes to limit
# available load to 1 core/ 2GB mem 
c.SwarmSpawner.resource_spec = {
    'cpu_limit': int(4 * 1e9),
    'mem_limit': int(8192 * 1e6),
    'cpu_reservation': int(1 * 1e9),
    'mem_reservation': int(2048 * 1e6),
}

# Service that checks for inactive notebooks
# Defaults to kill services that hasen't been used for 2 hours
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python cull_idle_servers.py --timeout=7200'.split(),
    }
]
