FROM centos/python-36-centos7:20200403-5aefd30
LABEL io.k8s.description="S2I builder for custom Jupyter notebooks." \
      io.k8s.display-name="Jupyter Notebook" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jupyter" \
      io.openshift.s2i.scripts-url="image:///opt/app-root/builder" \
      io.vorcunus.description="Jupyter Notebook, JupyterLab+Git, OracleClient, Tensorflow" \
      maintainer="ozan@orcunus.com"

USER root
COPY . /tmp/src
RUN /tmp/src/install-oracleclient.sh
RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts
ENV XDG_CACHE_HOME=/opt/app-root/src/.cache

USER 1001
RUN /tmp/scripts/assemble

USER root
RUN /opt/app-root/bin/install-jupyterlab-ext.sh

USER 1001
CMD [ "/opt/app-root/builder/run" ]

# CHANGELOG
# 20200403: Added python modules upon request
# 20200410: Latest Python image, edit cull parameters
#
# BUILD: docker build -t docker.io/orcunuso/jupyternb-cpu:20200410 .
