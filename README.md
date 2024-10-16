# Proyecto de Medición de Temperatura con Termistores

## Descripción
Este proyecto tiene como objetivo medir la temperatura utilizando termistores NTC. Se utiliza un sistema de adquisición de datos (DAQ) NI USB-6008 para realizar las mediciones y un conjunto de algoritmos en Python para procesar y visualizar los datos.

## Tabla de Contenidos
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Características
- Medición de temperatura precisa con termistores NTC.
- Grabación de datos en tiempo real en un archivo CSV.
- Visualización gráfica de las temperaturas medidas.
- Configuración flexible para múltiples sensores.

## Instalación y Requisitos
### 1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/nombre-del-repositorio.git
```
O Descarga el archivo zip y descomprimelo para ejecutarlo localmente.
### 2. Asegúrate de tener instalado Python 3.0 en adelante
Disponible en: https://www.python.org/downloads/ 
### 2.1 Asegúrate de tener instaladas las librerias de python adecuadas como nidaqmx y matplotlib
   ```bash
   pip install nidaqmx
   pip install matplotlib
```
### 3. Asegura de tener instalado NI-DAQ mx
Estos son los drivers de la tarjeta (versión recomendada: Q4 2024) en: https://www.ni.com/es/support/downloads/drivers/download.ni-daq-mx.html#549669

## Uso y Requisitos
1. Ejecutar archivo main.py
2. Ingresar datos de medición
3. Corroborar por errores de conexión y medición
   
