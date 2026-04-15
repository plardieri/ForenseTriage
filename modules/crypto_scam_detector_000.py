import re

class CryptoScamModule:
    def __init__(self):
        # Patrones para direcciones de criptomonedas
        self.patterns = {
            'BTC': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
            'ETH': r'\b0x[a-fA-F0-9]{40}\b',
            'TRX': r'\bT[A-Za-z1-9]{33}\b'
        }
        # Palabras detonantes de estafa (Scam Triggers)
        self.scam_keywords = ["inversión segura", "ganancia diaria", "recuperar cuenta", "soporte metamask"]

    def scan_content(self, text_data):
        findings = {"wallets": [], "scam_score": 0, "alerts": []}
        
        # 1. Buscar Wallets
        for coin, pattern in self.patterns.items():
            found = re.findall(pattern, text_data)
            if found:
                findings["wallets"].extend([(coin, addr) for addr in found])
                findings["scam_score"] += 20
        
        # 2. Análisis de Intención (Triage de Estafa)
        for word in self.scam_keywords:
            if word in text_data.lower():
                findings["scam_score"] += 15
                findings["alerts"].append(f"Palabra de riesgo detectada: {word}")
        
        # 3. Identificación de frases semilla (Simplificado)
        # Aquí se integraría una comparación contra el diccionario BIP39
        
        return findings