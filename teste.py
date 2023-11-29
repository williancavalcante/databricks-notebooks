from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

df = spark.read.table("hive_metastore.default.departments")
df.show()