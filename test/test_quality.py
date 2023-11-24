from pyspark.testing.utils import assertDataFrameEqual
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.getOrCreate()
# COMMAND ----------
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

# COMMAND ----------

def test_dataframe_equality():
        data = [("Alice", 1), ("Bob", 2)]
        df1 = spark.createDataFrame(data, ["name", "id"])
        df2 = spark.createDataFrame(data, ["name", "id"])

        assertDataFrameEqual(df1, df2)

# COMMAND ----------

def test_dataframe_filtering():
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    df = spark.createDataFrame(data, ["name", "id"])
    filtered_df = df.filter(df["id"] > 1)

    expected_data = [("Bob", 2), ("Charlie", 3)]
    expected_df = spark.createDataFrame(expected_data, ["name", "id"])

    assertDataFrameEqual(filtered_df, expected_df)

# COMMAND ----------
import time
r = 2+2
time.sleep(3)
print(r)
r = r + 2

def multiplica(r):
     s = r * 1000
     s = multiplica(s)