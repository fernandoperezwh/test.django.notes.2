## Instalar uWSGI y Nginx

```bash
sudo apt-get update
sudo apt-get install nginx uwsgi uwsgi-plugin-python3
```

## Configurar uWSGI

1. Crea un archivo de configuración para uWSGI en la raíz de tu proyecto de Django.
 ```bash
export WORKDIR=$(pwd)
export PROJECT_NAME=test.django.notes.2

touch $WORKDIR/$PROJECT_NAME/uwsgi.ini
```

Aquí tienes un ejemplo de cómo podría ser su contenido:

```ini
[uwsgi]
# Configuración básica
project = test_django_notes
base = /home/fernando/Escritorio/test.django.notes.2

# Punto de entrada de la aplicación
module = src.core.wsgi:application

# Configuración del socket
socket = /tmp/test_django_notes.sock
chmod-socket = 664
vacuum = true

# Configuración de procesos y threads
workers = 4
threads = 2
master = true
enable-threads = true

# Configuración del log
logto = /var/log/uwsgi/%n.log
```


2. Indicar a uwsgi que utilice el archivo de configuración.

Especificar la ubicación del archivo de configuración en el archivo de servicio de systemd para uWSGI.

```bash
sudo nano /etc/systemd/system/test_django_notes.service
```

Dentro del archivo, puedes agregar la siguiente configuración.
```bash
[Unit]
Description=uWSGI service for test_django_notes
After=network.target

[Service]
User=root
Group=root

WorkingDirectory=/home/fernando/Escritorio/test.django.notes.2
Environment="PATH=/home/fernando/.cache/pypoetry/virtualenvs/test.django.notes-dS2GDLp5-py3.6/bin"
ExecStart=/home/fernando/.cache/pypoetry/virtualenvs/test.django.notes-dS2GDLp5-py3.6/bin/uwsgi --ini /home/fernando/Escritorio/test.django.notes.2/uwsgi.ini

Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```




## Configurar Nginx

1. Crea un archivo de configuración para Nginx
```bash
touch /etc/nginx/sites-available/test_django_notes
```

Aquí tienes un ejemplo de cómo podría ser su contenido:
```text
server {
    listen 80;
    server_name djnotes.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/test_django_notes.sock;
    }
}

```

## Habilitar el archivo de configuración de Nginx

Crea un enlace simbólico del archivo de configuración que acabas de crear en el directorio `/etc/nginx/sites-available/test_django_notes`.
```bash
sudo ln -s /etc/nginx/sites-available/test_django_notes /etc/nginx/sites-enabled/
```


## Reiniciar uWSGI y Nginx

```bash
sudo systemctl restart test_django_notes
sudo systemctl restart nginx
```

