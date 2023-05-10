# Test Django Notes

Test Django Notes es un repositorio de prueba hecho en django diseñado para que puedas realizar notas personales como manuales

## Pasos para iniciar el proyecto desde cero

```bash
export WORKDIR=$(pwd)
export PROJECT_NAME=test.django.notes
mkdir -p $WORKDIR/$PROJECT_NAME

cd $WORKDIR/$PROJECT_NAME
touch README.md
```


Crear el entorno para instalar django con la configuración default
```bash
poetry init -n
```

Agregamos el django 3.2
```bash
poetry add django==3.2
```

Creamos un proyecto de django.
El proyecto lo nombraremos `src` y le indicamos que lo cree en este directorio.

```bash
django-admin startproject src .
```

Reestructurare el proyecto colocando los archivos de django en la carpeta core
```bash
# Crear el directorio core
mkdir -p $WORKDIR/$PROJECT_NAME/src/core
touch $WORKDIR/$PROJECT_NAME/src/__init__.py

# Mover los archivos 
mv $WORKDIR/$PROJECT_NAME/src/asgi.py $WORKDIR/$PROJECT_NAME/src/core/
mv $WORKDIR/$PROJECT_NAME/src/wsgi.py $WORKDIR/$PROJECT_NAME/src/core/
mv $WORKDIR/$PROJECT_NAME/src/urls.py $WORKDIR/$PROJECT_NAME/src/core/
mv $WORKDIR/$PROJECT_NAME/src/settings.py $WORKDIR/$PROJECT_NAME/src/core/
```

Por restructurar hay que cambiar los archivos `manage.py`, `src/asgi.py`, `src/wsgi.py` y `src/settings.py`

Comprobamos que funcione el proyecto
```bash
# Entramos al directorio
cd $WORKDIR/$PROJECT_NAME

# Levantamos el entorno y ejecutamos el manage
poetry shell
python manage.py runserver 0.0.0.0:8000
```




Una vez comprobado que funcione el proyecto, inicializamos el repositorio con Git.
```bash
git init
```

Creamos el archivo .gitignore con el contenido de la [siguiente url](https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore) para el archivo `.gitignore` de un proyecto de python.

```bash
# Entramos al directorio
cd $WORKDIR/$PROJECT_NAME

# Descargamos el archivo .gitignore para proyectos hechos en python
wget -O .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
```

Ejecutamos el siguiente comando para agregar al gitignore la instrucción de que ignore la base de datos
```bash
echo "# Local" >> .gitignore
echo "src/db.sqlite3" >> .gitignore
```

Ahora si agregemos los cambios al proyecto

```bash
git add .
git commit -m "init"
```

### Cambiamos el modelo del usuario de django por buenas practicas
Creamos la aplicación nts_account
```
mkdir -p src/apps/nts_account

python manage.py startapp nts_accounts ./src/apps/nts_account
```

Agregamos la clase del modelo User en el archivo `models.py`. A continuación agregamos la variable que define donde se encuentra nuestra clase
en el archivo de `src/core/settings.py` del proyecto

```bash
echo "AUTH_USER_MODEL = 'nts_account.User'" >> src/core/settings.py
```

A continuación agregamos nuestra aplicación en los `INSTALLED_APPS` que se encuentra en el archivo `src/core/settings.py`

Hacemos migración de este nuevo modelo. Y finalmente aplicamos la migración creada

```bash
python manage.py makemigrations
python manage.py migrate
```



## Iniciar proyecto

Cree el entorno e instale las dependencias con
```bash
poetry install
```

Realice las migraciones para generar la base de datos
```bash
python manage.py migrate
```

Crea un superusuario con el siguiente comando. Aqui se especifica que el email es `admin@example.com` y la contraseña `temporal1`
```bash
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=temporal1

python manage.py createsuperuser --name admin --noinput
```

