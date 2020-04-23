import os

port = int(os.environ.get('JUPYTER_NOTEBOOK_PORT', '8080'))

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = port
c.NotebookApp.open_browser = False
c.NotebookApp.quit_button = False

if os.environ.get('JUPYTERHUB_SERVICE_PREFIX'):
    c.NotebookApp.base_url = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')

################## JUPYTERPG ################

# https://jupyter-notebook.readthedocs.io/en/latest/config.html#options

tcKernelTimeout = int(os.environ.get('JUPYTERNB_KERNEL_TIMEOUT', '0'))
c.NotebookApp.shutdown_no_activity_timeout = 3601
c.MappingKernelManager.cull_idle_timeout = tcKernelTimeout
c.MappingKernelManager.cull_busy = False
c.MappingKernelManager.cull_connected = True
c.MappingKernelManager.cull_interval = 301

#############################################

password = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD')
if password:
    import notebook.auth
    c.NotebookApp.password = notebook.auth.passwd(password)
    del password
    del os.environ['JUPYTER_NOTEBOOK_PASSWORD']

image_config_file = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

if os.path.exists(image_config_file):
    with open(image_config_file) as fp:
        exec(compile(fp.read(), image_config_file, 'exec'), globals())
