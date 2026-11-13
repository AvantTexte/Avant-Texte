import os
import json
import time
import unittest

class TestPerformance(unittest.TestCase):
    def test_json_vocab_loading_speed(self):
        vocab_dir = "datos/vocab"
        start_time = time.perf_counter()
        
        count = 0
        if os.path.exists(vocab_dir):
            for fname in os.listdir(vocab_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(vocab_dir, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        count += 1
                        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        print(f"[BENCHMARK] Parseadas {count} fichas de vocabulario en {elapsed_ms:.2f} ms")
        self.assertLess(elapsed_ms, 500.0, "La carga del dataset supera los 500ms permitidos.")

    def test_index_file_latency(self):
        index_path = "datos/index.json"
        if os.path.exists(index_path):
            start_time = time.perf_counter()
            with open(index_path, "r", encoding="utf-8") as f:
                index_data = json.load(f)
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"[BENCHMARK] Indice principal cargado en {elapsed_ms:.2f} ms")
            self.assertLess(elapsed_ms, 100.0, "El indice principal tarda mas de 100ms en abrirse.")

if __name__ == "__main__":
    unittest.main()
