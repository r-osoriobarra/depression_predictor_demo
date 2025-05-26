# train_and_export_model.py - FIXED VERSION
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

# Load the data
print(f"Loading dataset from {dataset_path}...")
df = pd.read_csv(dataset_path)

print(f"Original dataset shape: {df.shape}")
print(f"Original columns: {list(df.columns)}")

# DATA CLEANING - Remove irrelevant columns and filter data
print("\n--- DATA CLEANING ---")

# Remove columns that don't contribute to prediction (but KEEP Age!)
columns_to_remove = ['City', 'Work Pressure', 'Job Satisfaction', 'id']
for col in columns_to_remove:
    if col in df.columns:
        print(f"Removing '{col}' column. Shape before: {df.shape}")
        df = df.drop(col, axis=1)
        print(f"Shape after removing '{col}': {df.shape}")

# Filter to only students BUT KEEP THE PROFESSION COLUMN FOR NOW
if 'Profession' in df.columns:
    print(f"Filtering only 'Student' in Profession. Rows before: {len(df)}")
    df = df[df['Profession'] == 'Student']
    print(f"Rows after filtering 'Student': {len(df)}")
    
    # NOW remove the Profession column since all rows are 'Student'
    print(f"Removing 'Profession' column after filtering. Shape before: {df.shape}")
    df = df.drop('Profession', axis=1)
    print(f"Shape after removing 'Profession': {df.shape}")

# Remove problematic values from Sleep Duration and Financial Stress
columns_to_clean = ['Sleep Duration', 'Financial Stress']
for col in columns_to_clean:
    if col in df.columns:
        print(f"Cleaning problematic values from {col}. Rows before: {len(df)}")
        df = df[~df[col].isin(['Others', '?', 'unknown'])]
        print(f"Rows after cleaning {col}: {len(df)}")

print(f"\nFinal dataset shape after cleaning: {df.shape}")
print(f"Final columns for training: {list(df.columns)}")

# VERIFICATION: Check that we have the expected columns
expected_final_columns = [
    'Gender', 'Age', 'Academic Pressure', 'CGPA', 'Study Satisfaction', 
    'Sleep Duration', 'Dietary Habits', 'Degree', 
    'Have you ever had suicidal thoughts ?', 'Work/Study Hours', 
    'Financial Stress', 'Family History of Mental Illness', 'Depression'
]

actual_columns = list(df.columns)
print(f"Expected columns: {expected_final_columns}")
print(f"Actual columns: {actual_columns}")

# Check if Age is present
if 'Age' not in df.columns:
    print("❌ ERROR: Age column is missing!")
    exit(1)
else:
    print("✅ Age column is present")

# Separate features (X) and target (y)
X = df.drop('Depression', axis=1)
y = df['Depression']

# Save the columns used for prediction
feature_columns = X.columns.tolist()

print(f"\nFeature columns that will be used: {feature_columns}")

# Identify column types
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(exclude=['int64', 'float64']).columns.tolist()

print(f"Numeric features: {numeric_features}")
print(f"Categorical features: {categorical_features}")

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# CRITICAL POINT: Explicitly train the preprocessor
print("\nFitting the preprocessor...")
preprocessor.fit(X_train)

# Apply preprocessing
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# Train the model
print("\nTraining the model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_transformed, y_train)

# Evaluate the model
train_score = model.score(X_train_transformed, y_train)
test_score = model.score(X_test_transformed, y_test)
print(f"\nTrain accuracy: {train_score:.4f}")
print(f"Test accuracy: {test_score:.4f}")

# VERIFY: Check if model has feature_importances_
if hasattr(model, 'feature_importances_'):
    print("✅ Model has feature_importances_ attribute")
else:
    print("❌ Model does NOT have feature_importances_ attribute")
    print(f"Model type: {type(model)}")

# Display feature importance
if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
    feature_names = preprocessor.get_feature_names_out()
    
    # Create importance dataframe
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print(f"\nTop 10 most important features:")
    print(importance_df.head(10))
else:
    print("Skipping feature importance analysis - model doesn't support it")

# Create the 'model' directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save the model, preprocessor, and feature columns
print("\nSaving model, preprocessor, and feature columns...")
with open('model/depression_model.pkl', 'wb') as f_model:
    pickle.dump(model, f_model)

# Save the TRAINED preprocessor
with open('model/preprocessor.pkl', 'wb') as f_pre:
    pickle.dump(preprocessor, f_pre)

# Save the list of feature columns
with open('model/feature_columns.pkl', 'wb') as f_cols:
    pickle.dump(feature_columns, f_cols)

print("\n=== MODEL TRAINING COMPLETED SUCCESSFULLY ===")
print("Files saved:")
print("- model/depression_model.pkl")
print("- model/preprocessor.pkl") 
print("- model/feature_columns.pkl")
print(f"\nFeature columns saved: {feature_columns}")
print("\nYou can now use these files in your Streamlit application.")