#!/bin/bash

set -x
set -eo pipefail

#mkdir -p /opt/app-root/src/PV/packages

echo '############## Installing JupyterLab-Git ##############'

jupyter labextension install @jupyterlab/git
pip install --upgrade jupyterlab-git
jupyter serverextension enable --py jupyterlab_git --sys-prefix
jupyter lab build

chown 1001:0 -R /opt/app-root/lib/python3.6/site-packages
chown 1001:0 -R /opt/rh/rh-python36/root/usr/lib/python3.6/site-packages

