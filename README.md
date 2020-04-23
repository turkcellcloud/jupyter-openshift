# Jupyter on OpenShift 3.11

This repository includes software and configurations as a result of my efforts to provide datascientists a highly customizable, powerfull and a secure platform on OpenShift Container Platform 3.11. Before going deeper into it, first things first, I've greatly inspired from two repos maintained by @GrahamDumpleton, [JupyterHub Quickstart](https://github.com/jupyter-on-openshift/jupyterhub-quickstart) and [Jupyter Notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks), then I created my own images and many configurations. I might have moved away from some of the Graham's good-practices in return for meeting other needs of the solution and I'm still working on them.

Secondly, I'm aware of Open Data Hub project but still manually trying to put all the pieces together is a great way to experience and learn more about the components like JupyterHub, JupyterLab, KubeSpawner, etc.

<center><b>This documentation is still in progress</b></center>

## What is Jupyter Notebook and JupyterHub

The notebook extends the console-based approach to interactive computing in a qualitatively new direction, providing a web-based application suitable for capturing the whole computation process: developing, documenting, and executing code, as well as communicating the results. The Jupyter notebook combines two components:

* **A web application**: a browser-based tool for interactive authoring of documents which combine explanatory text, mathematics, computations and their rich media output.
* **Notebook documents**: a representation of all content visible in the web application, including inputs and outputs of the computations, explanatory text, mathematics, images, and rich media representations of objects.

[JupyterHub](https://github.com/jupyterhub/jupyterhub) is the best way to serve [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html) for multiple users. It can be used in a classes of students, a corporate data science group or scientific research group. It is a multi-user Hub that spawns, manages, and proxies multiple instances of the single-user Jupyter notebook server.

## Prepare JupyterHub and Notebook images

The first step in deploying JupyterHub is to prepare a notebook image and the image for JupyterHub. The contents of the images and Dockerfiles exists in ``images`` folder. What we need to do is to build them and push to a private registry or Docker Hub. These images are CentOS based and usually I prefer to use specific tags so please check for the most recent tags of related base images from [Docker Hub](https://hub.docker.com/).

```
cd ./images/jupyterhub
docker build -t <registry>/<user>/jupyterhub:<tag> .
docker push <registry>/<user>/jupyterhub:<tag>

cd ../jupyternb
docker build -t <registry>/<user>/jupyternb:<tag> .
docker push <registry>/<user>/jupyternb:<tag>
```

JupyterHub image is pretty straightforward, these is nothing fancy about it, it will install regular python modules related with JupyterHub. But notebook image is a little bit more customized and complicated, apart from python modules, Oracle client binaries, tensorflow and JupyterLab (with ``git`` extension) installations also take place. As a result of this, we have a pretty big image, so you are warned :)  

If you are unsure of how to build these images, feel free to use the ones that exist in the template. 

## Deploy JupyterHub environment

The pre-requisities of deploying a JupyterHub environment is as follows:

* A functional OpenShift 3.11 environment. If an OpenShift cluster at your disposal does not exist, you can have a look at [Minishift](https://www.okd.io/minishift/).
* A linux machine to run your ``oc`` commands which can access to your OpenShift cluster.
* Web server certificates named ``jupyter-ssl.crt`` and ``jupyter-ssl.key``.
* Internet access from your linux machine.
* A quiet place without any distractions.

Start with cloning the repository, creating the namespace, importing the template and creating a new application from the template. There are more parameters in template config, so don't miss to check and adapt according to your environment.

```
git clone https://github.com/vOrcunus/jupyter-openshift.git
oc new-project datascience --display-name="MY JUPYTER PROJECT"
oc -n datascience apply -f ./config/template-jupyterhub.yaml
oc -n datascience new-app --template jupyterhub --param APPLICATION_NAME=jupyter
oc status
```

A postgresql and the jupyterhub pod should have been created. I've defined the replica count of jupyterhub as zero because we need to do some extra configs in order to prevent it from getting erros. These configurations are;

* Give ``anyuid`` permission to jupyter service account. This is required for running cull-idle service on jupyterhub otherwise it errors out.
* Create configMap that includes most of our jupyterhub customizations.
* Copy your certificate files, inject them to jupyterhub pod via secrets. 

```
oc adm policy add-scc-to-user anyuid system:serviceaccount:datascience:jupyter
oc -n datascience apply -f ./config/configmap-jupyterhub.yaml
oc -n datascience create secret tls jupyter-ssl --cert jupyter-ssl.crt --key jupyter-ssl.key
oc -n datascience set volume dc/jupyter --add -t secret -m /opt/app-root/share/jupyterhub/ssl --name certs --secret-name jupyter-ssl
```

Now we are ready to spin up our jupyterhub pod.

```
oc -n datascience scale dc/jupyter --replicas=1
```  
