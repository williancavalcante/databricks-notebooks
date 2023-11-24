# Databricks notebook source
from heimdall import StorageContext
import unittest
# COMMAND -----------

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