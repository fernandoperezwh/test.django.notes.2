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
```bash
cd $WORKDIR/$PROJECT_NAME
mkdir -p $WORKDIR/$PROJECT_NAME/src/apps/nts_account

python manage.py startapp nts_accounts ./src/apps/nts_account
```

Agregamos la clase del modelo User en el archivo `src/apps/nts_account/models.py`. 
```python
# python packages
import uuid
# django packages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as UserManager_
from django.db import models


class UserManager(UserManager_):
    """ Custom UserManager for the custom user model

    """
    def _create_user(self, email, password, **extra_fields):
        """ Create and save a user with the given email and password.

        """
        if not email:
            raise ValueError('User must have a email address')
        if not password:
            raise ValueError('User must have a password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create a user

        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create a super user

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    # Remove the first_name and last_name cols in the AbstractUser model
    first_name = None  # :type: ignore
    last_name = None  # :type: ignore

    # Username is really the user's "public id" field
    username = models.UUIDField(
        verbose_name='Public id',
        db_column='public_id',
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text='Public user identifier',
    )

    # First and last name do not cover name patterns around the globe
    name = models.CharField(
        verbose_name='User full name',
        blank=True,
        max_length=255,
    )

    # User's email address
    email = models.EmailField(
        verbose_name='Email address',
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        },
    )

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    def get_full_name(self):
        """Return the full name."""
        return self.name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name.split(' ')[0]

    def get_initials(self):
        """
        Return the initials of the user's name.
        Eg. Foo Bar Baz --> FB
        """
        name_words = self.name.split(' ')[:2]
        return ''.join(map(lambda x: x[0], name_words))

    def __str__(self):
        return self.name
```


A continuación agregamos la variable que define donde se encuentra nuestra clase
en el archivo de `src/core/settings.py` del proyecto

```bash
echo "AUTH_USER_MODEL = 'nts_account.User'" >> $WORKDIR/$PROJECT_NAME/src/core/settings.py
```

Editamos el name y label de nuestra aplicación en el archivo `src/apps/nts_account/apps.py`
```python
from django.apps import AppConfig


class NtsAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.nts_account'
    label = 'nts_account'

```

A continuación agregamos nuestra aplicación `'src.apps.nts_account'` en los `INSTALLED_APPS` que se encuentra en el archivo `src/core/settings.py`

Hacemos migración de este nuevo modelo. Y finalmente aplicamos la migración creada

```bash
cd $WORKDIR/$PROJECT_NAME

python manage.py makemigrations
python manage.py migrate
```



## Iniciar proyecto

Cree el entorno e instale las dependencias con
```bash
cd $WORKDIR/$PROJECT_NAME
poetry install
```

Realice las migraciones para generar la base de datos
```bash
python manage.py migrate
```

Crea un superusuario con el siguiente comando. Aqui se especifica que el email es `admin@example.com` y la contraseña `temporal1`
```bash
export WORKDIR=$(pwd)
export PROJECT_NAME=test.django.notes
cd $WORKDIR/$PROJECT_NAME

export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=temporal1

python manage.py createsuperuser --name admin --noinput
```

Ejecute el proyecto con el comando
```bash
# Entramos al directorio
cd $WORKDIR/$PROJECT_NAME

# Levantamos el entorno y ejecutamos el manage
poetry shell
python manage.py runserver 0.0.0.0:8000
```