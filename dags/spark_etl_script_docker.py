import requests
import json
from pyspark.sql import SparkSession
from pyspark import SQLContext
from pyspark.sql import functions as F
from decouple import config

azure_access_key = config('AZURE_ACCESS_KEY')
azure_account_name = config('AZURE_ACCOUNT_NAME')

from pyspark.sql.types import StructType, StructField, StringType
schema = StructType([StructField("id", StringType(), True),
                     StructField("brewery_type", StringType(), True),
                     StructField("city", StringType(), True),
                     StructField("state", StringType(), True),
                     StructField("country", StringType(), True),
                     StructField("latitude", StringType(), True),
                     StructField("longitude", StringType(), True)])

spark = SparkSession \
    .builder \
    .appName("DataExtraction") \
    .config("spark.hadoop.fs.azure.skipUserGroupMetadataDuringInitialization","true") \
    .getOrCreate() 

spark.conf.set("fs.azure.account.key.ariflowtestconn.dfs.core.windows.net","1AavlD+FDubX8VlN9XKhNSMvfxGD2ZQY0Xz916Li2pszg8pT0z1vIYmdxa/6QldU4K28DKBjhMSj+AStihRZbw==")
# hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3a.access.key", aws_access_key)
# hadoop_conf.set("fs.s3a.secret.key", aws_secret_key)
# hadoop_conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
# hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

response = requests.get("https://api.openbrewerydb.org/v1/breweries")
response = response.json()
print(response)
#data = response.text
#sparkContext = spark.sparkContext
#RDD = sparkContext.parallelize([data])
#raw_json_dataframe = spark.read.json(RDD)
deptColumns = ["id","brewery_type",'city','state','country','latitude','longitude']
dataframe=spark.createDataFrame(data=response, schema=schema)
print("a")

#raw_json_dataframe.printSchema()
#raw_json_dataframe.createOrReplaceTempView("Mutual_benefit")

#dataframe = raw_json_dataframe.withColumn("data", F.explode(F.col("data"))) \
#        .withColumn('meta', F.expr("meta")) \
 #       .select("data.*", "meta.*")
        
#dataframe.show(100, False)
## NOTE This line requires Java 8 instead of Java 11 work it to work on Airflow
## We are saving locally for now.
dataframe.write.parquet(f"abfss://teste@{azure_account_name}.dfs.core.windows.net/raw/a.parquet",mode='overwrite')
#dataframe.write.format('csv').option('header','true').save('s3a://sparkjobresult/output',mode='overwrite')
df=spark.read.csv(f"abfss://teste@ariflowtestconn.dfs.core.windows.net/data.csv")
df.show()