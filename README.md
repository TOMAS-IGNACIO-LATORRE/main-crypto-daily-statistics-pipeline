# main-crypto-daily-statistics-pipeline


## Tabla de contenidos



## Introducción

Este proyecto se encarga de la implementación de un pipeline ETL (Extract, Transform, Load) diseñado para obtener las cotizaciones de las principales criptomonedas por medio de extracciones diarias del día anterior. El pipeline utiliza ![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white) para la contenerización, Apache Airflow para la orquestación, Amazon Redshift como almacenamiento de datos y cómputo. A su vez, se utiliza Python como lenguaje principal a la hora de gestionar el pipeline extrayendo datos de APIs financieras(CoinGecko y CoinMarketCap), transformando en una etapa posterior y cargando en bases de datos para su uso analítico.

El objetivo principal de este proyecto es proporcionar un análisis diario de las cotizaciones de las criptomonedas más relevantes, obteniendo los datos del día anterior finalizado. A medida que las criptomonedas ganan popularidad y su uso se expande, es esencial monitorear sus precios y tendencias. Este análisis ayuda a los inversores y a otros agentes económicos a tomar decisiones informadas en un entorno altamente volátil.






