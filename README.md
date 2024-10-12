# main-crypto-daily-statistics-pipeline

## 📚 Tabla de contenidos

1. [Introducción](#Introducción)
2. [Pipeline de datos](#Pipeline-de-datos)
3. [Implementación](#Implementación)

## 🌐 Introducción

Este proyecto se encarga de la implementación de un pipeline ETL (Extract, Transform, Load)  diseñado para obtener las cotizaciones de las principales criptomonedas por medio de extracciones diarias del día anterior. El pipeline utiliza ![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white) para la contenerización, ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-green?logo=apache-airflow&logoColor=white) para la orquestación, ![Amazon Redshift](https://img.shields.io/badge/Amazon%20Redshift-red?logo=amazon-redshift&logoColor=white) como almacenamiento de datos y cómputo. A su vez, se utiliza ![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white) como lenguaje principal a la hora de gestionar el pipeline extrayendo datos de APIs financieras(CoinGecko y CoinMarketCap), transformando en una etapa posterior y cargando en bases de datos para su uso analítico.

El objetivo principal de este proyecto es proporcionar un análisis diario de las cotizaciones de las criptomonedas más relevantes, obteniendo los datos del día anterior finalizado. A medida que las criptomonedas ganan popularidad y su uso se expande, es esencial monitorear sus precios y tendencias. Este análisis ayuda a los inversores y a otros agentes económicos a tomar decisiones informadas en un entorno altamente volátil.

## 📈 Pipeline de datos

En este proceso de ETL, se utilizó la visión de Databricks conocido como [Lakehouse](https://www.databricks.com/glossary/data-lakehouse). En esta visión, se implementa de la siguiente forma:

- **Staging**: Se realiza un proceso de extracción de tipo **batch processing** donde se obtienen los datos en bruto extraídos directamente de las APIs de CoinGecko y CoinMarketCap. Estos datos se almacenan en archivos de tipo Parquet para su fácil manipulación y lectura.
- **Silver**: En esta etapa, los datos se le realizan un proceso de enriquecimiento de datos, donde se combinan, limpian y transforman. Un ejemplo de estas transformaciones son agregaciones de columnas, modificaciones de tipos de datos, entre otras. Se obtienen dichos parquet transformados y se aplica una carga intermedia en Amazon RedShift para crear un conjunto de datos intermedios que facilitan el análisis.
- **Gold**: Aquí se generan los conjuntos de datos finales que están listos para el análisis y la visualización. En este caso, se emplea Amazon RedShift para su análisis.

 A continuación, comparto una imagen que muestra esta estructura efectuada por DataBricks:

![](https://blog.bismart.com/hs-fs/hubfs/Arquitectura_Medallion_Pasos.jpg?width=1754&height=656&name=Arquitectura_Medallion_Pasos.jpg)

### 📁 Fuente de datos hacia Staging
Para todas las fuentes, se utilizó código en Python para obtener datos de las APIs. Estas son las siguientes:
  -  [CoinMarkerCap API](https://coinmarketcap.com/api/documentation/v1/): Desde esta fuente de datos obtenemos los datos descriptivos de cada criptomoneda. Entre ellos, podemos mencionar symbol, name, category (coin o token), description, logo, website y reddit. Esta API se accede mediante una API KEY, es necesario dirigirse a este [link](https://coinmarketcap.com/api/), es necesario registrarse y de esta manera, podemos tener acceso a su API gratuita. En el caso de solicitudes, tiene un límite de 333 request por día que significa un promedio de 10.000 llamadas por mes, esto se puede escalar si accedes a una versión pro de la API.

- [CoinGecko API](https://docs.coingecko.com/reference/introduction): Se trata de una API de acceso público y gratuito sin necesidad de usar una API KEY. Desde esta fuente, extraemos los precios de apertura, de cierre, precios máximos y mínimos de cada cryptomoneda con frecuencia de media hora. La misma  impone límites en la frecuencia de las solicitudes que se trata de **100 solicitudes por minuto**.

> Es importante destacar que esta API de CoinGecko proporciona la información del día anterior para cada tipo de cambio, no datos históricos de precios. Si se desea obtener datos de días anteriores, se debe modificar el parámetro days ubicado en la carpeta staging en el archivo `api_extract_data.py`.

A nivel técnico, en el DAG se cuenta con función `run_staging` que se encarga de ejecutar esta extracción. Esta a su vez, llamada a dos funciones:

- 


Podemos visualizar este proceso en el siguiente esquema:

![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/Source_to_Staging.png)

### 📁 Staging hacia Silver

### 📁 Silver hacia Gold

### 🚨 Alertas - email

## 🛠️ Implementación

###  Requisitos previos

Se debe tener instalado las siguientes herramientas:

- Python
- Docker Desktop
- Airflow
- AWS Redshift

## Setup