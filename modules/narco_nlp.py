import joblib
import spacy
import os

class NarcoClassifier:
    def __init__(self, model_path='models/narco_model.pkl', vectorizer_path='models/vectorizer.pkl'):
        # 1. Cargar el modelo de IA y el vectorizador entrenados
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
        else:
            self.model = None
            self.vectorizer = None
            print("[!] Advertencia: Modelo no encontrado. Use el modo entrenamiento primero.")

        # 2. Cargar modelo de lenguaje español para limpieza de texto
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except:
            print("[!] Error: No se encontró el modelo de spacy 'es_core_news_sm'.")

    def _preprocess(self, text):
        """Limpia el texto: quita mayúsculas, signos y lleva a la raíz (lema)."""
        doc = self.nlp(text.lower())
        # Filtra stop-words y puntuación, quedándose con la raíz de las palabras
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

    def analyze(self, text_list):
        """
        Recibe una lista de mensajes y devuelve los sospechosos con su probabilidad.
        """
        if not self.model or not self.vectorizer:
            return {"error": "Modelo no cargado"}

        findings = []
        
        for raw_text in text_list:
            clean_text = self._preprocess(raw_text)
            vectorized_text = self.vectorizer.transform([clean_text])
            
            # Obtener probabilidad de la clase 1 (Narcotráfico)
            prob = self.model.predict_proba(vectorized_text)[0][1]
            
            # Solo reportar si supera un umbral (ej. 70%)
            if prob > 0.70:
                findings.append({
                    "text": raw_text,
                    "confidence": round(prob * 100, 2),
                    "tags": ["Transaccional", "Jerga Detectada"]
                })

        return {
            "total_analyzed": len(text_list),
            "suspicious_count": len(findings),
            "hits": findings
        }

# Ejemplo de uso rápido
if __name__ == "__main__":
    # Datos de prueba
    test_chats = [
        "¿A cuánto el gramo de la blanca?",
        "Mañana paso a jugar playstation",
        "Punto de entrega en la plaza a las 20hs"
    ]
    
    # Nota: Este ejemplo fallará si no has guardado primero el .pkl
    classifier = NarcoClassifier()
    print(classifier.analyze(test_chats))