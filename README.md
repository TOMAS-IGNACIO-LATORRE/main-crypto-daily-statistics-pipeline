# main-crypto-daily-statistics-pipeline

## 📚 Tabla de contenidos

1. [Introducción](#-introducción)
2. [Implementación](#%EF%B8%8F-implementación) 
3. [Pipeline de datos](#-pipeline-de-datos)
4. [Futuras Mejoras](#-futuras-mejoras)


## 🌐 Introducción

Este proyecto se encarga de la implementación de un pipeline ETL (Extract, Transform, Load)  diseñado para obtener las cotizaciones de las principales criptomonedas por medio de extracciones diarias del día anterior. El pipeline utiliza ![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white) para la contenerización, ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-green?logo=apache-airflow&logoColor=white) para la orquestación, ![Amazon Redshift](https://img.shields.io/badge/Amazon%20Redshift-red?logo=amazon-redshift&logoColor=white) como almacenamiento de datos y cómputo. A su vez, se utiliza ![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white) como lenguaje principal a la hora de gestionar el pipeline extrayendo datos de APIs financieras(CoinGecko y CoinMarketCap), transformando en una etapa posterior y cargando en bases de datos para su uso analítico.

El objetivo principal de este proyecto es proporcionar un análisis diario de las cotizaciones de las criptomonedas más relevantes, obteniendo los datos del día anterior finalizado. A medida que las criptomonedas ganan popularidad y su uso se expande, es esencial monitorear sus precios y tendencias. Este análisis ayuda a los inversores y a otros agentes económicos a tomar decisiones informadas en un entorno altamente volátil.

## 🛠️ Implementación

###  Requisitos previos

Se debe tener instalado las siguientes herramientas:

- Python
- Docker Desktop
- Airflow
- AWS Redshift

## Setup
Los pasos a seguir son los siguientes:
 #### 1. Clonar este repositorio
   ```bash
    git clone https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline.git
  ```
 #### 2. Navegar en este directorio:
```bash
cd main-crypto-daily-statistics-pipeline
```

#### 3. Configurar las variables del entorno en un archivo `.env`:
 
-  [CoinMarkerCap API](https://coinmarketcap.com/api/documentation/v1/): Esta API se accede mediante una API KEY, es necesario dirigirse a este [link](https://coinmarketcap.com/api/), registrarse y de esta manera, podemos tener acceso a su API KEY de forma gratuita.

```bash
# UID AIRFLOW
AIRFLOW_UID=50000 # Colocar siempre mismo valor

# APIs keys
api_key_coinmarketcap = 'complete_your_api_key'

# DB Redshift 
HOST_REDSHIFT=your_host
PORT_REDSHIFT=your_port
DBNAME_REDSHIFT=your_dbname
USER_REDSHIFT=your_username
PASSWORD_REDSHIFT=your_password

# Email-Alerting
ALERT_EMAIL = 'complete_your_email' # El proceso envia un mail de alerta para avisar status del pipeline, unicamente admite gmail
```

#### 4. Correr Makefile 

Este proceso efectúa una automatización del pipeline en lo que se refiere a la construcción de las imagenes de Docker, levantar los servicios de Docker compose y la creación de directorios junto con la configuración del entorno de Airflow.

```bash
make all
```
#### 5. Acceder a la UI de Airflow

Visita http://localhost:8080 en tu navegador. En el mismo vamos a tener que completar lo siguiente:

`usuario`: airflow

`Contraseña`: airflow

Podemos visualizarlo con más atención en este imagen:

![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/airflow_2.png)

A continuación, debemos configurar las variables de entorno para nuestro mail de gmail, para eso:

Admin > + Connections > + Add new record

En el mismo, se deben completar los siguientes registros:

 - `Connection Id`: smtp_default
 - `Connection Type`: Email
 - `Host`: smtp.gmail.com
 - `Login`: 'complete_your_email'
 - `Contraseña`: Para obtener la contraseña, deben generar una contraseña para aplicaciones en gmail. Para eso, deben acceder a https://myaccount.google.com/apppasswords y generar una contraseña
 - `Port`: 587
 - `Extra`: 
{
  "timeout": 30,
  "retry_limit": 5,
  "disable_tls": false,
  "disable_ssl": true
}

Para finalizar, debemos prender encender el DAG que diga `crypto_price_dags` y esperar a las 00:00:00 del día siguiente para que corra o ejecutar manualmente el mismo.

> Si quieren aplicarlo para mails de outlook pueden visitar el siguiente video https://www.youtube.com/watch?v=D18G7hW8418 que me ayudo a aprender esta configuración

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

- `api_extract_data.py`: El archivo contiene dos funciones principales para interactuar con las APIs de CoinGecko y CoinMarketCap. La primera función, get_crypto_ohlc_data, obtiene los precios OHLC de una criptomoneda para una fecha específica, organizando los datos en un DataFrame de pandas. La segunda función, create_crypto_table, extrae información descriptiva sobre una criptomoneda, manejando errores de solicitudes excesivas y asegurando una recuperación adecuada de datos.

- `parquet_staging.py`: El archivo define una función llamada parquet_create_staging, que se encarga de crear archivos Parquet para los precios diarios de criptomonedas y sus perfiles. Utiliza las funciones get_crypto_ohlc_data y create_crypto_table para obtener datos de criptomonedas, concatenando la información en DataFrames de pandas y manejando excepciones si no se recuperan datos válidos. Al final, guarda los DataFrames en archivos Parquet en una ubicación específica, asegurando que se creen exitosamente.


Podemos visualizar este proceso en el siguiente esquema:

![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/Source_to_Staging_Visual.png)

### 📁 Staging hacia Silver

Se encarga de transformar e enriquecer los datos provenientes desde las fuentes de datos cargando en Amazon Redshift. Se emplea lo indicado en el siguiente pipeline:

![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/Staging_to_Silver.png)


A nivel técnico, en el DAG se cuenta con función `run_silver`. Este proceso utiliza las siguientes funciones:

- `create_tables_redshift.py`: Este script crea tablas en una base de datos de Amazon Redshift, asegurándose de que cada tabla se cree solo si no existe previamente. Las tablas incluyen crypto_description, dim_date, daily_crypto_prices, y crypto_volatility_and_performance, las cuales están diseñadas para almacenar información sobre criptomonedas, datos de precios diarios y métricas de rendimiento. Además, el script utiliza claves foráneas para establecer relaciones entre las tablas.

- `parquet_Silver.py`: Este script en Python carga y actualiza archivos Parquet que contienen datos relacionados con precios diarios de criptomonedas, información de criptomonedas y fechas. En resumen hace las siguientes cosas:

   A) Carga de Archivos Parquet: Se define una función load_parquet_files que toma una fecha como argumento y retorna tres DataFrames: precios diarios de criptomonedas, datos de criptomonedas y un DataFrame de fechas.Los archivos Parquet se cargan desde rutas específicas que incluyen la fecha proporcionada.

  B) Renombrado de Columnas y Reemplazo de Valores: Al cargar el DataFrame de precios diarios, la columna stock_symbol se renombra a symbol, y se reemplazan ciertos valores en esta columna para estandarizar la nomenclatura (por ejemplo, 'bitcoin' se cambia a 'BTC').

  C) Actualización del Archivo Plata de Precios Diarios: Si existe un archivo de precios diarios en la carpeta "Silver", se carga y se verifica si hay nuevas fechas en el DataFrame cargado. Si hay nuevas fechas, se concatenan y se guardan de nuevo en el archivo Parquet; de lo contrario, se informa que no hay nuevos datos.

  D) Actualización del Archivo Plata de Datos de Criptomonedas: De manera similar, se verifica si el archivo de datos de criptomonedas existe y se actualiza con nuevas filas. Si hay filas nuevas, se concatenan y se guardan.

  E) Generación de un DataFrame de Fechas: Se crea un DataFrame dim_date_df que contiene fechas únicas extraídas de los precios diarios, añadiendo columnas para el año, mes, número de semana, día, y otras métricas relevantes.

  F) Actualización del Archivo Plata de Fechas: Se realiza una verificación y actualización del archivo de la tabla de fechas de manera similar a las anteriores, añadiendo fechas nuevas si es necesario.

- `table_insert_sql.py`: Este script en Python se encarga de la inserción y actualización de datos relacionados con criptomonedas en una base de datos, utilizando el patrón Slowly Changing Dimension (SCD) Tipo 2 y operaciones de inserción para datos de fechas y precios diarios. Teniendo las siguientes funciones: 

A) **insert_crypto_description_scd2:**   Implementar SCD Tipo 2 en la tabla crypto_description, lo que permite mantener un historial de los cambios en los registros de criptomonedas.

B) **insert_date_data:** Insertar registros de fechas en la tabla dim_date sin duplicar los existentes tomando en cuenta todas las fechas para que si la persona quiere cambiar para traer más fechas, no duplique las fechas.

C) **insert_daily_crypto_prices:** Insertar o actualizar los precios diarios de criptomonedas en la tabla daily_crypto_prices.


### 📁 Silver hacia Gold

En este proceso, se hace un análisis por el día entero de las cotizaciones de las principales criptomonedas. Esto permite tener algunos KPIs que permitan tener una vista rápida de los rendimientos del día de ejecución. Se aplica por medio del siguiente script:

- `crypto_volability_and_performance.py`: El script calcula y registra métricas financieras diarias para criptomonedas. Primero, verifica si ya existen datos para una fecha específica en la tabla crypto_volatility_and_performance. Luego, obtiene los precios diarios de criptomonedas y calcula métricas como volatilidad, retorno y rango. Finalmente, inserta los resultados en la base de datos. Esto permite analizar el rendimiento de las criptomonedas de manera efectiva.

A su vez, con la siguiente visual muestra este traspaso desde Silver hacia Gold:

![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/Silver_to_Gold.png)

### 🚨 Alertas - email

Nos indica si la ejecución del pipeline de Airflow fue exitosa o si en alguno de los pasos anteriores, nos encontramos con algún problema. Podemos encontrarla dentro del DAG con el task_id= `send_email`.

A continuación adjuntamos dos ejemplos:

- ✅ Ejecución exitosa:
![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/email_exitoso.png)

- ❌Ejecución fallida:
![](https://github.com/TOMAS-IGNACIO-LATORRE/main-crypto-daily-statistics-pipeline/blob/main/Errores_en_el_mail.png)

## 🔔 Next Steps
- Optimización de la ingestión de datos históricos con procesamiento distribuido.
- Buscar APIs para poder incorporar el volumen del mercado diario de cada una de las criptomonedas y aprovechar para sacar métricas de esta variable numérica.
