import re

class CryptoScamModule:
    def __init__(self):
        # 1. Diccionario de Expresiones Regulares para Wallets
        self.patterns = {
            'Bitcoin (P2PKH)': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
            'Ethereum/ERC-20': r'\b0x[a-fA-F0-9]{40}\b',
            'Monero': r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b',
            'Litecoin': r'\b[LM][a-km-zA-HJ-NP-Z1-9]{26,33}\b'
        }

        # 2. Palabras clave de Ingeniería Social (Scam Triggers)
        self.scam_indicators = [
            "frase semilla", "seed phrase", "private key", "llave privada",
            "ganancia garantizada", "duplicar inversion", "soporte tecnico",
            "validar billetera", "meta mask", "trust wallet", "binance login"
        ]

    def _check_bip39_seed(self, text):
        """
        Detecta posibles frases semilla de 12 o 24 palabras.
        En una versión avanzada, compararías contra el diccionario BIP39 de 2048 palabras.
        """
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        # Si hay una secuencia de 12 o 24 palabras seguidas, es altamente sospechoso
        if len(words) == 12 or len(words) == 24:
            return True
        return False

    def scan_content(self, text_data):
        """
        Realiza el triaje del texto buscando wallets y patrones de estafa.
        """
        findings = {
            "wallets_detected": [],
            "scam_score": 0,
            "alerts": [],
            "risk_level": "Bajo"
        }

        # A. Búsqueda de Direcciones de Billeteras
        for coin_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text_data)
            if matches:
                for addr in set(matches): # Usamos set para evitar duplicados
                    findings["wallets_detected"].append({"type": coin_name, "address": addr})
                    findings["scam_score"] += 25  # Encontrar una wallet sube el score

        # B. Análisis de Ingeniería Social
        for indicator in self.scam_indicators:
            if indicator in text_data.lower():
                findings["scam_score"] += 15
                findings["alerts"].append(f"Indicador de fraude: '{indicator}'")

        # C. Verificación de Frases Semilla
        if self._check_bip39_seed(text_data):
            findings["scam_score"] += 50
            findings["alerts"].append("Posible FRASE SEMILLA (Seed Phrase) detectada")

        # D. Clasificación de Riesgo Final
        if findings["scam_score"] >= 75:
            findings["risk_level"] = "Crítico"
        elif findings["scam_score"] >= 40:
            findings["risk_level"] = "Alto"
        elif findings["scam_score"] > 0:
            findings["risk_level"] = "Medio"

        return findings

# Ejemplo de prueba
if __name__ == "__main__":
    scanner = CryptoScamModule()
    test_data = "Hola, soy del soporte de Meta Mask. Para validar su cuenta envíe su frase semilla o transfiera a 0x71C2496123456789ABCDEF123456789ABCDEF012"
    print(scanner.scan_content(test_data))
    