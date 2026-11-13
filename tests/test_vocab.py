import unittest
import json
import os
import glob

class TestProyectoLiseurVocab(unittest.TestCase):
    def test_index_json_exists_and_valid(self):
        index_path = 'datos/index.json'
        self.assertTrue(os.path.exists(index_path), "El archivo datos/index.json no existe.")
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIsInstance(data, list, "datos/index.json debe contener una lista.")
        self.assertGreater(len(data), 0, "datos/index.json no debe estar vacío.")

    def test_vocab_items_structure(self):
        files = glob.glob('datos/vocab/*.json')
        self.assertGreater(len(files), 0, "Debe haber archivos JSON en datos/vocab/")
        
        required_keys = ['id', 'capitulo', 'frances', 'espanol', 'tipo']
        for file_path in files[:50]:
            with open(file_path, 'r', encoding='utf-8') as f:
                item = json.load(f)
            for key in required_keys:
                self.assertIn(key, item, f"Falta la clave '{key}' en {file_path}")

    def test_frontend_files_exist(self):
        for fname in ['index.html', 'styles.css', 'app.js']:
            self.assertTrue(os.path.exists(fname), f"Falta el archivo frontend {fname}")

if __name__ == '__main__':
    unittest.main()
