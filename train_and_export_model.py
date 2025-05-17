# train_and_export_model.py corregido
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define the path to the dataset
dataset_path = os.path.join('data', 'student_depression_dataset.csv')

# Carga los datos
print(f"Loading dataset from {dataset_path}...")
df = pd.read_csv(dataset_path)

# Separar características (X) y objetivo (y)
# Asumimos que la columna objetivo es 'Depression'
X = df.drop('Depression', axis=1)
y = df['Depression']

# Guardar las columnas usadas para predicción
feature_columns = X.columns.tolist()

# Identificar tipos de columnas
numeric_features = X.select_dtypes(
    include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(
    exclude=['int64', 'float64']).columns.tolist()

print(f"Numeric features: {numeric_features}")
print(f"Categorical features: {categorical_features}")

# Crear preprocesador
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# PUNTO CRÍTICO: Entrena explícitamente el preprocesador
print("Fitting the preprocessor...")
preprocessor.fit(X_train)

# Aplicar preprocesamiento
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# Entrenar el modelo
print("Training the model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_transformed, y_train)

# Evaluar el modelo
train_score = model.score(X_train_transformed, y_train)
test_score = model.score(X_test_transformed, y_test)
print(f"Train accuracy: {train_score:.4f}")
print(f"Test accuracy: {test_score:.4f}")

# Crear el directorio 'model' si no existe
os.makedirs('model', exist_ok=True)

# Guardar el modelo
print("Saving model, preprocessor, and feature columns...")
with open('model/depression_model.pkl', 'wb') as f_model:
    pickle.dump(model, f_model)

# Guardar el preprocesador ENTRENADO
with open('model/preprocessor.pkl', 'wb') as f_pre:
    pickle.dump(preprocessor, f_pre)

# Guardar la lista de columnas
with open('model/feature_columns.pkl', 'wb') as f_cols:
    pickle.dump(feature_columns, f_cols)

print("Model, preprocessor, and feature columns exported successfully!")
