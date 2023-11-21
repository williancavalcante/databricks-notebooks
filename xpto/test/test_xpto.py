from databricks.connect.session import DatabricksSession as SparkSession
from databricks.sdk.core import Config
from pyspark.testing.utils import assertDataFrameEqual
from pyspark.sql.functions import *
from pyspark.sql.types import *
import unittest

config = Config(profile='DEFAULT', cluster_id='1017-032629-beha6p1')
spark = SparkSession.builder.sdkConfig(config).getOrCreate()

def test_dataframe_from_table():
        # Lendo o DataFrame da tabela (ajuste este comando para sua fonte de dados)
        df = spark.read.table("hive_metastore.default.departments")

        # Dados esperados
        expected_data = [(1, "Administration"), (2, "Human Resource"), (3, "Engineering")]
        # Schema para o DataFrame
        schema = "id INT, name STRING"

        # Criar DataFrame esperado
        expected_df = spark.createDataFrame(expected_data, schema)

        # Assert
        assertDataFrameEqual(df, expected_df)

def test_dataframe_equality():
        data = [("Alice", 1), ("Bob", 2)]
        df1 = spark.createDataFrame(data, ["name", "id"])
        df2 = spark.createDataFrame(data, ["name", "id"])

        assertDataFrameEqual(df1, df2)

def test_dataframe_filtering():
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    df = spark.createDataFrame(data, ["name", "id"])
    filtered_df = df.filter(df["id"] > 1)
    expected_data = [("Bob", 2), ("Charlie", 3)]
    expected_df = spark.createDataFrame(expected_data, ["name", "id"])

    assertDataFrameEqual(filtered_df, expected_df)