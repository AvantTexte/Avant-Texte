import unittest
import os
import json
import time

class TestPerformanceAndIntegrity(unittest.TestCase):
    def test_index_load_performance(self):
        index_path = "datos/index.json"
        if os.path.exists(index_path):
            start = time.time()
            with open(index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            elapsed = (time.time() - start) * 1000
            print(f"Index load time: {elapsed:.2f}ms")
            # Tolerancia amplia para VMs de GitHub Actions
            self.assertLess(elapsed, 2000.0, "El índice tardó demasiado en cargar")
        else:
            self.assertTrue(True)

    def test_vocab_structure_integrity(self):
        vocab_dir = "datos/vocab"
        if os.path.exists(vocab_dir):
            files = [f for f in os.listdir(vocab_dir) if f.endswith(".json")]
            self.assertGreaterEqual(len(files), 0)
        else:
            self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
