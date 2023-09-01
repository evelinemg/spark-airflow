# Docker: Airflow, Spark, Jupyter Notebook, Azure


### Sobre as imagens
#### Airflow:
- Dockerfile.Airflow: utiliza a versão [apache/airflow:latest-python3.9](https://hub.docker.com/layers/apache/airflow/latest-python3.9/images/sha256-f5dd54399c66eb93e481730efffa66eb002114c10a251de0edeac9bc322cf8ea?context=explore) e faz a instalação de pacotes para a execução do job spark.
- docker-compose.Airflow.yaml: baseada na [versão oficial](https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml) e configurada para usar a imagem "airflow-spark"


#### Spark:
- DockerFile.Spark: utiliza a imagem [bitnami/spark:3.4.1](https://hub.docker.com/layers/bitnami/spark/3.4.1/images/sha256-b1044b4d44db305452948f67747ebf92587c64cd54ffa2a41dc24dc1ee6002e3?context=explore) é feito o downloads dos jars para conexão com Azure.
- docker-compose.Spark: Constroe o Spark Master e n-Spark Workers a partir da imagem "spark-air". E cria um container a partir da image jupyter/pyspark-notebook:latest


### Instruções

#### Clonar o repositório

```
 git clone https://github.com/evelinemg/spark-airflow 
 ```
#### Gera a imagem Spark

```
docker build -f Dockerfile.Spark -t spark-air
```

#### Gera imagem Airflow
```
docker build -f Dockerfile.Airflow -t airflow-spark
```
#### Cria containers
```
docker-compose -f docker-compose.Spark.yaml -f docker-compose.Airflow.yaml up -d
```