import hashlib
import os
import imagehash
from PIL import Image

class MASIDetector:
    def __init__(self):
        # En un entorno real, aquí cargarías los hashes desde un JSON o SQLite de Autopsy
        # Simulamos una base de datos local de "Hashes Conocidos"
        self.known_sha256 = ["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"]
        self.known_phash = ["8c3a3a3a3a3a3a3a"] # Ejemplo de hash perceptual

    def calculate_sha256(self, file_path):
        """Calcula el hash SHA-256 de un archivo para coincidencia exacta."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def calculate_phash(self, image_path):
        """Calcula el hash perceptual para detectar imágenes similares/editadas."""
        try:
            with Image.open(image_path) as img:
                return str(imagehash.phash(img))
        except Exception:
            return None

    def scan_directory(self, directory_path):
        """Escanea una carpeta y clasifica archivos según su nivel de riesgo."""
        hits = []
        
        # Extensiones de imagen comunes
        img_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # 1. Verificación por SHA-256 (Cualquier archivo)
                file_sha = self.calculate_sha256(file_path)
                if file_sha in self.known_sha256:
                    hits.append({
                        "file": file,
                        "method": "SHA-256",
                        "match": True,
                        "risk": "Crítico"
                    })

                # 2. Verificación por pHash (Solo imágenes)
                if file.lower().endswith(img_extensions):
                    file_phash = self.calculate_phash(file_path)
                    if file_phash and file_phash in self.known_phash:
                        hits.append({
                            "file": file,
                            "method": "pHash",
                            "match": True,
                            "risk": "Muy Alto"
                        })

        return {
            "total_hits": len(hits),
            "details": hits
        }

# Pruebas unitarias del módulo
if __name__ == "__main__":
    detector = MASIDetector()
    # Resultado esperado: un diccionario con los hallazgos confirmados
    print(detector.scan_directory("./test_evidence"))