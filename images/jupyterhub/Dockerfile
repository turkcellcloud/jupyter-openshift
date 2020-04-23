FROM centos/python-36-centos7:20200403-5aefd30
LABEL io.k8s.display-name="JupyterHub" \
      io.k8s.description="JupyterHub." \
      io.openshift.tags="builder,python,jupyterhub" \
      io.openshift.s2i.scripts-url="image:///opt/app-root/builder" \
      io.vorcunus.description="JupyterHub Image v1.1.0, no UI customization" \
      maintainer="ozan@orcunus.com"

USER root
COPY . /tmp/src
RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    mv /tmp/src/.s2i/bin /tmp/scripts

USER 1001
ENV NPM_CONFIG_PREFIX=/opt/app-root \
    PYTHONPATH=/opt/app-root/src
RUN /tmp/scripts/assemble

CMD [ "/opt/app-root/builder/run" ]

