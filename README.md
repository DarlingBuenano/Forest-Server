# Forest-Server
Servidor web con API-RESTful para la detección de especies de árboles en bosques tropicales

## Instalación del entorno virtual
1. Instalar virtualenv
```bash
pip install virtualenv
```

2. Configurar entorno virtual
```bash
python -m venv ./venv
```


## Instalación de dependencias
```bash
pip install -r requirements.txt
```


## Instalación del proyecto
1. Iniciar un proyecto Django
```bash
django-admin startproject forest_server
```

2. Cambiar la configuración general
```python
# setting.py
ALLOWED_HOSTS = ['127.0.0.1', '*']
TIME_ZONE = 'America/Guayaquil'
LANGUAGE_CODE = 'es-es'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static'),
```

3. Cambiar la configuración de la base de datos
```python
# setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```