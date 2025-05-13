import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.impute import SimpleImputer

# Suppress warnings
warnings.filterwarnings('ignore')


class StudentDepressionPredictor:
    def __init__(self, filepath):

        print("=== STUDENT DEPRESSION PREDICTION PROJECT ===\n")

        # Load and explore data
        self.df = self.load_and_explore_data(filepath)

        # Clean data
        self.df = self.clean_data(self.df)

        # Visualize data
        self.visualize_data(self.df)

        # Prepare data for modeling
        self.X_train, self.X_test, self.y_train, self.y_test, self.preprocessor = self.prepare_data(
            self.df)

        # Train the model
        self.model = self.train_and_evaluate_model(
            self.X_train, self.y_train, self.X_test, self.y_test, self.preprocessor)

        # Analyze feature importance
        self.feature_importance = self.analyze_feature_importance(self.model)

        print("\n=== MODEL TRAINING COMPLETED ===")

    def load_and_explore_data(self, filepath):
        # Load data
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully. Shape: {df.shape}")

        # Missing values analysis
        missing = df.isnull().sum()
        missing_percentage = (missing / len(df) * 100).round(2)

        if missing.sum() > 0:
            print("\nMissing values summary:")
            missing_df = pd.DataFrame({
                'Count': missing,
                'Percentage (%)': missing_percentage
            })
            print(missing_df[missing_df['Count'] > 0])
        else:
            print("\nNo missing values in the dataset.")

        # Target variable distribution
        print("\nTarget variable distribution (Depression):")
        print(df['Depression'].value_counts())
        print(
            f"Percentage of depression cases: {df['Depression'].mean()*100:.2f}%")

        print("\n--- DESCRIPTIVE STATISTICS FOR KEY VARIABLES ---")

        # Variables for statistics
        stat_variables = [
            'Age',
            'Academic Pressure',
            'CGPA',
            'Study Satisfaction',
            'Work/Study Hours',
            'Depression'
        ]

        # Statistics table
        stats_df = df[stat_variables].describe().T

        # Reformatting table
        stats_table = pd.DataFrame({
            'Variable': stats_df.index,
            'Mean': stats_df['mean'].round(2),
            'Std': stats_df['std'].round(2),
            'Min': stats_df['min'].round(2),
            'Median': stats_df['50%'].round(2),
            'Max': stats_df['max'].round(2)
        })

        print("\nStatistics for Key Variables:")
        print(stats_table.to_string(index=False))

        return df

    def clean_data(self, df):

        print("\n--- DATA CLEANING ---")
        # Remove columns city, work pressure and job satisfaction
        columns_to_remove = ['City', 'Work Pressure', 'Job Satisfaction']
        for col in columns_to_remove:
            if col in df.columns:
                print(f"Removing '{col}' variable. Shape before: {df.shape}")
                df = df.drop(col, axis=1)
                print(f"Shape after removing '{col}': {df.shape}")

        # Select only students
        if 'Profession' in df.columns:
            print(
                f"Filtering only 'Student' in Profession. Rows before: {len(df)}")
            df = df[df['Profession'] == 'Student']
            print(f"Rows after filtering 'Student': {len(df)}")

        # Remove "Others", "?" and "unknown"
        columns_to_clean = ['Sleep Duration', 'Financial Stress']
        for col in columns_to_clean:
            if col in df.columns:
                print(
                    f"Removing problematic values from {col}. Rows before: {len(df)}")
                df = df[~df[col].isin(['Others', '?', 'unknown'])]
                print(f"Rows after cleaning {col}: {len(df)}")

        # Remove ID column
        if 'id' in df.columns:
            df = df.drop('id', axis=1)

        print(f"\nFinal dataset shape after cleaning: {df.shape}")
        return df

    def ensure_images_dir(self):

        if not os.path.exists('images'):
            os.makedirs('images')
            print("Created 'images' directory for saving visualizations")
        return os.path.join(os.getcwd(), 'images')

    def visualize_data(self, df):

        print("\n--- DATA VISUALIZATION ---")

        # image directory
        images_dir = self.ensure_images_dir()

        # Create a copy of the dataframe with Depression labels for visualization
        viz_df = df.copy()
        viz_df['Depression_Label'] = viz_df['Depression'].map(
            {0: 'No', 1: 'Yes'})

        custom_palette = {'Yes': 'orange', 'No': 'blue'}

        # Categorical variables
        categorical_vars = [
            'Academic Pressure',
            'Sleep Duration',
            'Have you ever had suicidal thoughts ?',
            'Financial Stress',
            'Family History of Mental Illness',
            'Dietary Habits'
        ]

        plt.figure(figsize=(20, 15))
        for i, var in enumerate(categorical_vars, 1):
            plt.subplot(2, 3, i)
            sns.countplot(x=var, hue='Depression_Label',
                          data=viz_df,
                          palette=custom_palette)
            plt.title(f'{var} vs Depression')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

        plt.savefig(os.path.join(images_dir, 'categorical_variables.png'))
        plt.close()

        # Numerical variables boxplots
        numerical_vars = ['Age', 'CGPA', 'Work/Study Hours']

        plt.figure(figsize=(15, 5))
        for i, var in enumerate(numerical_vars, 1):
            plt.subplot(1, 3, i)
            sns.boxplot(x='Depression_Label', y=var,
                        data=viz_df,
                        palette=custom_palette)
            plt.title(f'{var} Distribution by Depression')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'numerical_boxplots.png'))
        plt.close()

        # Correlation Heatmap
        plt.figure(figsize=(12, 10))
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        correlation_matrix = numeric_df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
                    linewidths=0.5, fmt='.2f', square=True, center=0)
        plt.title('Correlation Heatmap of Numerical Variables')
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'correlation_heatmap.png'))
        plt.close()

        # CGPA Distribution by Depression Status
        plt.figure(figsize=(10, 6))
        sns.histplot(data=viz_df, x='CGPA', hue='Depression_Label',
                     palette=custom_palette,
                     kde=True, bins=20,
                     element='step', common_norm=False)
        plt.title('CGPA Distribution by Depression Status')
        plt.xlabel('CGPA')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'cgpa_distribution.png'))
        plt.close()

        # Age vs Work/Study Hours Scatter Plot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=viz_df, x='Age', y='Work/Study Hours',
                        hue='Depression_Label',
                        palette=custom_palette, alpha=0.7)
        plt.title('Age vs Work/Study Hours by Depression Status')
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'age_workhours_scatter.png'))
        plt.close()

        print(f"Visualizations saved in the 'images' directory")

    def prepare_data(self, df):

        print("\n--- DATA PREPARATION ---")

        # Ensure Depression is the target variable
        if 'Depression' not in df.columns:
            raise ValueError("Depression column not found in the dataset")

        X = df.drop('Depression', axis=1)
        y = df['Depression']

        # Identify column types
        numeric_features = X.select_dtypes(
            include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(
            include=['object']).columns.tolist()

        print(f"Numeric features: {numeric_features}")
        print(f"Categorical features: {categorical_features}")

        # Create preprocessors
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline([
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]), numeric_features),
                ('cat', Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]), categorical_features)
            ]
        )

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)

        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")

        return X_train, X_test, y_train, y_test, preprocessor

    def train_and_evaluate_model(self, X_train, y_train, X_test, y_test, preprocessor):

        print("\n--- MODEL TRAINING ---")

        # images directory if it doesn't exist
        images_dir = self.ensure_images_dir()

        # pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        # Parameters for search
        param_grid = {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5],
            'classifier__min_samples_leaf': [1, 2]
        }

        # Hyperparameter search using gridsearch - optimiazation
        print("Performing hyperparameter tuning (this may take a while)...")
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
        grid_search.fit(X_train, y_train)

        print("\nBest hyperparameters found:")
        print(grid_search.best_params_)

        # Evaluation
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1]

        print("\n--- MODEL EVALUATION ---")
        print("\nClassification report:")
        print(classification_report(y_test, y_pred))

        # ROC
        plt.figure(figsize=(8, 6))
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, color='darkorange', lw=2,
                 label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.savefig(os.path.join(images_dir, 'roc_curve.png'))
        plt.close()

        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.savefig(os.path.join(images_dir, 'confusion_matrix.png'))
        plt.close()

        return best_model

    def analyze_feature_importance(self, model):

        print("\n--- FEATURE IMPORTANCE ANALYSIS ---")

        # Create images directory if it doesn't exist
        images_dir = self.ensure_images_dir()

        if hasattr(model[-1], 'feature_importances_'):
            importances = model[-1].feature_importances_

            # Get feature names from preprocessor
            feature_names = model[0].get_feature_names_out()

            # Adjust lengths if necessary
            if len(importances) != len(feature_names):
                min_len = min(len(importances), len(feature_names))
                importances = importances[:min_len]
                feature_names = feature_names[:min_len]

            # Create importance dataframe
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)

            # Visualize
            plt.figure(figsize=(12, 8))
            sns.barplot(x='Importance', y='Feature',
                        data=importance_df.head(20))
            plt.title('Top 20 Most Important Features')
            plt.tight_layout()
            plt.savefig(os.path.join(images_dir, 'feature_importance.png'))
            plt.close()

            print("Top 10 most important features:")
            print(importance_df.head(10))
            print(f"\nVisualization saved in the 'images' directory")

            return importance_df

        return None

    def predict_depression(self, new_data, case_number=1):

        print("\n=== DEPRESSION RISK ASSESSMENT ===")

        # Convert input to DataFrame if it's a dictionary
        if isinstance(new_data, dict):
            new_data = pd.DataFrame([new_data])

        # Verify profession if column exists
        if 'Profession' in new_data.columns and (new_data['Profession'] != 'Student').any():
            print("WARNING: Only 'Student' profession is supported by this model")
            new_data = new_data[new_data['Profession'] == 'Student']

            if len(new_data) == 0:
                raise ValueError("No student data provided for prediction")

        # Make a copy of the original data for display purposes
        display_data = new_data.copy()

        # Remove any columns not used in the original training
        original_columns = self.X_train.columns.tolist()

        # Ensure all original columns are present
        for col in original_columns:
            if col not in new_data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Select only the columns used in training
        new_data = new_data[original_columns]

        # Prediction
        try:
            # Predict probabilities
            probability = self.model.predict_proba(new_data)[:, 1]

            # Calculate feature contributions
            importances = self.model[-1].feature_importances_
            feature_names = self.model[0].get_feature_names_out()

            # Create a dataframe of feature importances
            feature_contrib_df = pd.DataFrame({
                'Feature': feature_names,
                'Contribution': importances
            }).sort_values('Contribution', ascending=False)

            # Clean feature names (remove 'cat__' and split multiple categories)
            def clean_feature_name(name):
                # Remove 'cat__' prefix
                clean_name = name.replace('cat__', '')
                # Replace multiple categories with a single category
                if '_' in clean_name and clean_name.count('_') > 1:
                    parts = clean_name.split('_')
                    clean_name = f"{parts[0]} ({parts[-1]})"
                return clean_name

            # Determine risk level
            if probability[0] < 0.3:
                risk_level = "LOW"
                recommendation = "Continue maintaining good mental health practices."
            elif probability[0] < 0.6:
                risk_level = "MEDIUM"
                recommendation = "Consider seeking support or counseling."
            else:
                risk_level = "HIGH"
                recommendation = "Strongly recommended to seek professional help."

            # Print overall depression probability
            print(
                f"\nCase {case_number}: Depression Probability = {probability[0]:.2%} (Risk Level: {risk_level})")
            print(f"Recommendation: {recommendation}")

            # Print student information
            print("\nStudent Information:")
            for column, value in display_data.iloc[0].items():
                print(f" {column}: {value}")

            # Print feature contributions with cleaned names
            print("\nFeature Contribution to Depression Risk:")
            for _, row in feature_contrib_df.head(10).iterrows():
                # Clean the feature name
                clean_name = clean_feature_name(row['Feature'])
                print(f" {clean_name}: {row['Contribution']*100:.2f}%")

            return probability

        except Exception as e:
            print(f"Error during prediction: {e}")
            print("Please ensure all input data matches the training data format.")
            return None
