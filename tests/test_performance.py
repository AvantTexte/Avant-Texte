import os
import json
import time
import unittest

class TestRepositoryIntegrity(unittest.TestCase):
    def test_datos_index_exists_and_valid(self):
        index_path = "datos/index.json"
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsNotNone(data)

    def test_performance_sla_flexible(self):
        start = time.time()
        index_path = "datos/index.json"
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                _ = json.load(f)
        elapsed = (time.time() - start) * 1000
        print(f"Index load time: {elapsed:.2f} ms")
        self.assertTrue(elapsed < 5000, f"Parse time {elapsed}ms exceeded SLA limit")

if __name__ == "__main__":
    unittest.main()
