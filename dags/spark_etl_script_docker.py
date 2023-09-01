import requests
import json
from pyspark.sql import SparkSession
from pyspark import SQLContext
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import functions as F
from decouple import config
from constants import base_url, params, container

azure_access_key = config('AZURE_ACCESS_KEY')
azure_account_name = config('AZURE_ACCOUNT_NAME')

schema = StructType([StructField("id", StringType(), True),
                     StructField("brewery_type", StringType(), True),
                     StructField("city", StringType(), True),
                     StructField("state", StringType(), True),
                     StructField("country", StringType(), True),
                     StructField("latitude", StringType(), True),
                     StructField("longitude", StringType(), True)])

def makeSparkSession(name="DataExtraction", master="local"):
    spark= SparkSession \
        .builder \
        .appName(name) \
        .config("spark.master",master) \
        .config("spark.hadoop.fs.azure.skipUserGroupMetadataDuringInitialization","true") \
        .getOrCreate()

    spark.conf.set(f"fs.azure.account.key.{azure_account_name}.dfs.core.windows.net", f"{azure_access_key}")
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def getApi(base_url, params, response=[]):
    try:
        api_response=requests.get(base_url,params).json()
        
        if not api_response:
            return response
            
        response.extend(api_response)
        params['page']+=1
        
        return getApi(base_url,params,response)
    
    except Exception as e:
        raise Exception(f"Error! {e}")


def makeDfAndSparkSession():
    spark=makeSparkSession()
    response=getApi(base_url,params)
    df=spark.createDataFrame(data=response)
    return df, spark


if __name__ == '__main__':
    df,spark=makeDfAndSparkSession()
    df.show()
    df.write.parquet(f"abfss://{container}@{azure_account_name}.dfs.core.windows.net/raw/openbrewerydb",mode='overwrite')
    spark.stop()