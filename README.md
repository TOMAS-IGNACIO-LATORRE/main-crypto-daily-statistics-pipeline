# main-crypto-daily-statistics-pipeline


## 📚 Tabla de contenidos

1. [Introducción](#Introducción)
2. [Pipeline de datos](#Pipeline-de-datos)
3. [Implementación](#Implementación)

## 🌐 Introducción

Este proyecto se encarga de la implementación de un pipeline ETL (Extract, Transform, Load) diseñado para obtener las cotizaciones de las principales criptomonedas por medio de extracciones diarias del día anterior. El pipeline utiliza ![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white) para la contenerización, ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-green?logo=apache-airflow&logoColor=white) para la orquestación, ![Amazon Redshift](https://img.shields.io/badge/Amazon%20Redshift-red?logo=amazon-redshift&logoColor=white) como almacenamiento de datos y cómputo. A su vez, se utiliza ![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white) como lenguaje principal a la hora de gestionar el pipeline extrayendo datos de APIs financieras(CoinGecko y CoinMarketCap), transformando en una etapa posterior y cargando en bases de datos para su uso analítico.

El objetivo principal de este proyecto es proporcionar un análisis diario de las cotizaciones de las criptomonedas más relevantes, obteniendo los datos del día anterior finalizado. A medida que las criptomonedas ganan popularidad y su uso se expande, es esencial monitorear sus precios y tendencias. Este análisis ayuda a los inversores y a otros agentes económicos a tomar decisiones informadas en un entorno altamente volátil.

## 📈 Pipeline de datos

En este proceso de ETL, se utilizó la visión de Databricks conocido como [Lakehouse](https://www.databricks.com/glossary/data-lakehouse). En esta visión, se inicia con las diversas **fuentes de datos** las cuales se extraen hacia una primera etapa conocida como **Bronze o Staging** en la cual se guardan los datos tal cual provienen de esta fuente de datos primaria. Luego, esa fuente primaria se le lleva hacia una segunda etapa conocida como **Silver** en la cual se aplican ciertas transformaciones como agregado de columnas, modificación de tipos de datos, entre otras más. Para finalizar, estos datos transformados se llevan hacia una etapa final conocida como **Gold** en la cual se disponibilizan los datos para emplear analítica sea mediante tableros de analítcas o modelos de Machine Learning. A continuación, comparto una imagen que muestra esta estructura:

![](https://blog.bismart.com/hs-fs/hubfs/Arquitectura_Medallion_Pasos.jpg?width=1754&height=656&name=Arquitectura_Medallion_Pasos.jpg)

### 📁 Fuente de datos hacia Staging
Para todas las fuentes, se utilizó código en Python para obtener datos de las APIs. Entre las APIs utiza

### 📁 Staging hacia Silver

### 📁 Silver hacia Gold

### Alertas - email

## 🛠️ Implementación

###  Requisitos previos

Se debe tener instalado las siguientes herramientas:

- Python
- Docker Desktop
- Airflow
- AWS Redshift

## Setup





