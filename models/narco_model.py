import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 1. Preparación de Datos (Dataset Sintético para tu Diplomatura)
# En un caso real, aquí cargarías un CSV con miles de ejemplos
data = {
    'texto': [
        "necesito 50 gramos de la blanca", "pasa por el punto de entrega",
        "tengo cristal disponible 24/7", "cuanto por el kilo de merca",
        "el envio llega mañana a la plaza", "quiero jugar al futbol",
        "nos vemos en el cine", "mañana hay examen de matematicas",
        "pasa por casa a tomar cafe", "compre pizza para cenar"
    ],
    'etiqueta': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0] # 1: Narco, 0: Normal
}

df = pd.DataFrame(data)

# 2. Preprocesamiento y Vectorización
# El TfidfVectorizer convierte el texto en una matriz numérica que la IA entiende
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['texto'])
y = df['etiqueta']

# 3. Entrenamiento del Modelo (Random Forest)
# Elegimos Random Forest porque es explicable y robusto
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Exportación de los Archivos .pkl
# Creamos la carpeta models si no existe
import os
if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/narco_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("[!] Archivos generados exitosamente en la carpeta /models/")
print(f"Palabras aprendidas: {len(vectorizer.get_feature_names_out())}")
