import os
import pickle
from src.depression_predictor import StudentDepressionPredictor

# Define the path to the dataset
dataset_path = os.path.join('data', 'student_depression_dataset.csv')

# Train the model using the StudentDepressionPredictor class
predictor = StudentDepressionPredictor(dataset_path)

# Create the output directory if it does not exist
os.makedirs('model', exist_ok=True)

# Export the trained model (Random Forest)
with open('model/depression_model.pkl', 'wb') as f_model:
    pickle.dump(predictor.model, f_model)

# Export the data preprocessor (ColumnTransformer)
with open('model/preprocessor.pkl', 'wb') as f_pre:
    pickle.dump(predictor.preprocessor, f_pre)

# Export the list of feature columns used during training
with open('model/feature_columns.pkl', 'wb') as f_cols:
    pickle.dump(predictor.X_train.columns.tolist(), f_cols)

print("Model, preprocessor, and feature columns exported successfully to the 'model/' directory.")
