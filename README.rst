===================
nbi-jupyter-service
===================

A docker swarm setup that

-----------
Get Started
-----------

To run this stack, simply execute the following command inside the repo
directory

    docker stack deploy --compose-file docker-compose.yml nbi-jupyter-service


To verify that the stack is now deployed and the services are being spawned do:

    docker stack ls
    docker services ls

The stack command should return that 2 services are running, in addition the
 `services` call should return that the jupyterhub and nginx service is
 running/preparing to run. In addition it describes which ports the service
 is accessible through the nginx front proxy e.g. port 80/443

============
Architecture
============

An overview of how the different components of the
nbi_jupyter_service interconnects can be seen below:

Coming soon ...