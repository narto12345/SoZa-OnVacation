# SoZa-OnVacation

Proyecto que contempla una página web tradicional, manejando también un módulo administrativo con autenticación básica.

## Prerrequisitos

1. Python versión 3.13.0

## Pasos de instalación-Ambiente virtual y dependencias

Una vez clonado o descargado el repositorio, deberá entrar al directorio raíz del proyecto y ejecutar los siguientes comandos:

Opcional. Instalar entorno virtual en Windows:

```bash
pip install virtualenv
```

1. Crear entorno virtual en Windows:

```bash
py -m venv venv
```

2. Activar entorno virtual en Windows:

```bash
venv/Scripts/Activate
```

3. Instalar módulos necesarios

```bash
pip install -r requirements.txt
```

## Ejecución de proyecto

Recuerde que se manejará django, por lo que deberá contar con él en su máquina.
Ejecute el siguiente comando para levantar el proyecto:

```bash
  py manage.py runserver *numeroDePuerto*
```
