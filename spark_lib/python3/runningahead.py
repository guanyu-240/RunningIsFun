from pyspark.sql import SparkSession

FILE_DELIMITER = "\t"

def loadFile(fileName, appName="RunningAhead"):
    spark = SparkSession.builder.appName(appName).getOrCreate()
    df = spark.read.option("header", "true")\
        .option("delimiter", "\t")\
        .option("inferSchema", "true")\
        .csv(fileName)
    return df

def showLog(dataFrame, count, truncate=False):
    dataFrame.show(count, truncate=False)