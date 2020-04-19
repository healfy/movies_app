# movies_app
Test video archive application
For the core logic used Python3 + Django + DRF
Database - MariaDB

### Helpful
In existing cluster you can automatically deploy this application
You need make client
``sudo apt-get install make``
After this run:
 * ``make build DEV=1`` - to build only docker file
 * ``make deploy DEV=1`` - to build and deploy into cluster

### Commands
``./run.sh`` - to start uwsgi, only work inside of container
``./run_celery.sh`` - to start celery
