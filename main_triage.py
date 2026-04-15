import os
import json
from datetime import datetime
# Importación de tus módulos personalizados
from modules.masi_detector import MASIDetector
from modules.narco_nlp import NarcoClassifier
from modules.crypto_scam import CryptoScamModule

class ForensicOrchestrator:
    def __init__(self, case_id, evidence_path):
        self.case_id = case_id
        self.evidence_path = evidence_path
        self.start_time = datetime.now()
        
        # Inicialización de motores
        self.masi_engine = MASIDetector()
        self.narco_engine = NarcoClassifier()
        self.crypto_engine = CryptoScamModule()

    def run_triage(self):
        print(f"[*] Iniciando Triaje IA - Caso: {self.case_id}")
        results = {
            "metadata": {
                "case_id": self.case_id,
                "date": str(self.start_time),
                "evidence_source": self.evidence_path
            },
            "findings": {}
        }

        # 1. Procesamiento de Texto (Chats, Emails, Logs)
        # Suponiendo que ya extrajiste el texto con una función auxiliar
        raw_text = self._extract_text_from_evidence()

        print("[+] Ejecutando análisis de Narcotráfico y Estafas...")
        results["findings"]["narco"] = self.narco_engine.analyze(raw_text)
        results["findings"]["crypto_scam"] = self.crypto_engine.scan_content(raw_text)

        # 2. Procesamiento de Imágenes (MASI)
        print("[+] Ejecutando análisis de archivos multimedia...")
        results["findings"]["masi"] = self.masi_engine.scan_directory(self.evidence_path)

        return self._generate_final_report(results)

    def _extract_text_from_evidence(self):
        # Aquí iría tu lógica de conexión con SQLite o lectura de .txt de FTK
        return "Texto extraído de la evidencia..."

    def _generate_final_report(self, results):
        report_name = f"Reporte_{self.case_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_name, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"[!] Triaje completado. Reporte generado: {report_name}")
        return results

# Ejecución del proyecto
if __name__ == "__main__":
    triage = ForensicOrchestrator(case_id="CONF-2026-001", evidence_path="./evidencia_exportada")
    triage.run_triage()

import imagehash
from PIL import Image

# Generar un hash perceptual que ignore cambios leves de edición
def generar_hash_robusto(path_imagen):
    hash_perceptual = imagehash.phash(Image.open(path_imagen))
    return str(hash_perceptual)

# Comparar contra tu "Lista Negra" local
