# Jupyter on OpenShift 3.11

This repository includes software and configurations as a result of my efforts to provide datascientists a highly customizable, powerfull and a secure platform on OpenShift 3.11.Before going deeper, first things first, I've greatly inspired from two repos maintained by @GrahamDumpleton [JupyterHub Quickstart](https://github.com/jupyter-on-openshift/jupyterhub-quickstart) and [Jupyter Notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks), then I created my own images and many configurations. I might have moved away from some of the Graham's good-practices in return for meeting other needs of the solution and I'm still working on them.

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
