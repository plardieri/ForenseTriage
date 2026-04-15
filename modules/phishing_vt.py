import requests
import hashlib
import base64

class PhishingVTModule:
    def __init__(self, api_key):
        """
        Requiere una API Key de VirusTotal (v3).
        """
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3/"
        self.headers = {"x-apikey": self.api_key}

    def check_url(self, url):
        """
        Verifica la reputación de una URL en VirusTotal.
        """
        try:
            # La API v3 requiere la URL en base64 (sin padding '=')
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            response = requests.get(f"{self.base_url}urls/{url_id}", headers=self.headers)
            
            if response.status_code == 200:
                attr = response.json()['data']['attributes']
                stats = attr['last_analysis_stats']
                return {
                    "url": url,
                    "malicious": stats['malicious'],
                    "suspicious": stats['suspicious'],
                    "harmless": stats['harmless'],
                    "reputation_score": attr.get('reputation', 0)
                }
            elif response.status_code == 404:
                return {"url": url, "status": "No encontrada en VT (Posiblemente nueva)"}
            return {"error": f"Error API: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def check_file_hash(self, file_path):
        """
        Calcula el hash SHA-256 localmente y consulta su reputación.
        Garantiza la confidencialidad al NO subir el archivo real.
        """
        try:
            # Cálculo del Hash SHA-256
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            file_hash = sha256_hash.hexdigest()
            response = requests.get(f"{self.base_url}files/{file_hash}", headers=self.headers)

            if response.status_code == 200:
                attr = response.json()['data']['attributes']
                stats = attr['last_analysis_stats']
                return {
                    "hash": file_hash,
                    "malicious": stats['malicious'],
                    "suspicious": stats['suspicious'],
                    "type": attr.get('type_description', 'unknown'),
                    "match": True
                }
            return {"hash": file_hash, "match": False, "status": "Archivo no detectado previamente"}
        except Exception as e:
            return {"error": str(e)}

# Prueba rápida
if __name__ == "__main__":
    # Sustituir por tu llave real en la documentación
    vt = PhishingVTModule(api_key="TU_LLAVE_AQUI")
    # print(vt.check_url("http://phishing-scam.com"))
    