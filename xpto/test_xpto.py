from databricks.connect.session import DatabricksSession as SparkSession
from databricks.sdk.core import Config
from pyspark.testing.utils import assertDataFrameEqual
from pyspark.sql.functions import *
from pyspark.sql.types import *
from heimdall import StorageContext
import unittest

config = Config(profile='DEFAULT', cluster_id='1017-032629-beha6p1')
spark = SparkSession.builder.sdkConfig(config).getOrCreate()

class TestStorageContext(unittest.TestCase):
 
    def test_initialization(self):

        test_cases = [
            {
                "params": {
                    "storage_account": "stpandoraprdheimdall",
                    "path": "/blobServices/default/containers/risco-abertura-infracao-pix/blobs/",
                    "blob": "2023_11_16_17_57_24_3rd_willian_cavalcante.csv",
                    "invocation_id": "f93199c3-dd33-4aad-ae8c-c8eefb0164c6"
                },
                "expected": {
                    "storage_account": "stpandoraprdheimdall",
                    "invocation_id": "f93199c3-dd33-4aad-ae8c-c8eefb0164c6",
                    "container": "risco-abertura-infracao-pix",
                    "blob": "2023_11_16_17_57_24_3rd_willian_cavalcante.csv"
                }
            },
            {
                "params": {
                    "storage_account": "stpandoraxpto",
                    "path": "/blobServices/default/containers/xpto/blobs/path1/paht2",
                    "blob": "2023_11_16_17_57_24_3rd_willian_cavalcante.csv",
                    "invocation_id": "123-abc"
                },
                "expected": {
                    "storage_account": "stpandoraxpto",
                    "invocation_id": "123-abc",
                    "container": "xpto",
                    "blob": "2023_11_16_17_57_24_3rd_willian_cavalcante.csv"
                }
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                storage_context = StorageContext(**case["params"])
                for attr, expected_value in case["expected"].items():
                    actual_value = getattr(storage_context, attr)
                    self.assertEqual(actual_value, expected_value)
    
    def test_extract_value(self):
        test_cases = [
            {
                "params": {
                    "pattern": r"containers/([^/]+)",
                    "text": "/blobServices/default/containers/risco-abertura-infracao-pix/blobs/"
                },
                "expected": "risco-abertura-infracao-pix"
            },
            {
                "params": {
                    "pattern": r"blobs/(.+)",
                    "text": "/blobServices/default/containers/risco-abertura-infracao-pix/blobs/myfile.csv"
                },
                "expected": "myfile.csv"
            }
        ]

        for case in test_cases:
            with self.subTest(case=case):
                result = StorageContext._extract_value(**case["params"])
                self.assertEqual(result, case["expected"])

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