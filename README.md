# Dcoker: Airflow, Spark, Jupyter Notebook

Projeto para o estudo de Airflow utilizando Spark Operators. Por enquanto faz a leitura da API e faz o loading no Azure Data Lake Storage Gen2.

![Arquitetura](/images/arquitetura.png "Arquitetura do Projeto")
### Sobre as imagens Docker
#### Airflow:
- Dockerfile.Airflow: utiliza a versão [apache/airflow:latest-python3.9](https://hub.docker.com/layers/apache/airflow/latest-python3.9/images/sha256-f5dd54399c66eb93e481730efffa66eb002114c10a251de0edeac9bc322cf8ea?context=explore) e faz a instalação de pacotes para a execução do job spark.
- docker-compose.Airflow.yaml: baseada na [versão oficial](https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml) e configurada para usar a imagem "airflow-spark"


#### Spark:
- DockerFile.Spark: utiliza a imagem [bitnami/spark:3.4.1](https://hub.docker.com/layers/bitnami/spark/3.4.1/images/sha256-b1044b4d44db305452948f67747ebf92587c64cd54ffa2a41dc24dc1ee6002e3?context=explore) é feito o downloads dos jars para conexão com Azure.
- docker-compose.Spark: Constroe o Spark Master e n-Spark Workers a partir da imagem "spark-air". E cria um container a partir da image jupyter/pyspark-notebook:latest


### Instruções

#### Clonar o repositório

```
 git clone https://github.com/evelinemg/spark-airflow.git
 ```
#### Gera a imagem Spark

```
docker build -f Dockerfile.Spark . -t spark-air
```

#### Gera imagem Airflow
```
docker build -f Dockerfile.Airflow . -t airflow-spark
```

#### Cria variáveis de ambiete
Cria arquivo ".env" e defina as variáveis como no exemplo
```
AIRFLOW_UID=33333
AIRFLOW_GID=0
AZURE_ACCESS_KEY=<storage key>
AZURE_ACCOUNT_NAME=<storage account name>
```
#### Cria containers
```
docker-compose -f docker-compose.Spark.yaml -f docker-compose.Airflow.yaml up -d
```
#### Conexão Spark-Airflow

[imagem]

### Spark Workers
Para adicionar mais workes ao projeto basta replicar o código abaixo no arquivo "docker-composer.Spark.yaml"
```
spark-worker-n:
    image: spark-air:latest
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark:7077
      - SPARK_WORKER_MEMORY=1G
      - SPARK_WORKER_CORES=1
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
      - AZURE_ACCESS_KEY=${AZURE_ACCESS_KEY}
      - AZURE_ACCOUNT_NAME=${AZURE_ACCOUNT_NAME}
```


### Referências
O projeto foi adaptado dos respositórios abaixo, deixe de sua estrelinha neles:

:star2: [yTek0](https://github.com/yTek01/docker-spark-airflow)

:star2: [cordon-thiago](https://github.com/cordon-thiago/airflow-spark)

:star2: [puckel](https://github.com/puckel/docker-airflow)

:star2: [pyjaime](https://github.com/pyjaime/docker-airflow-spark)