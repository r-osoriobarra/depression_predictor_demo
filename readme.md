# Student Depression Predictor

Prototype tool for predicting depression in students.  
Assessment 1 Project – ICT619 Murdoch University.
Rodrigo Osorio / Mia Song

## Project Structure

```
.
├── data
│   └── student_depression_dataset.csv
├── images/
├── src
│   ├── __init__.py
│   ├── data_validator.py
│   ├── depression_predictor.py
│   └── student_case_manager.py
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install using `requirements.txt`)

### Installation

1. Download the project files
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure the dataset is placed in the `data` directory as `student_depression_dataset.csv`

### Running the Program

Execute the main script from the project root directory:

```bash
python main.py
```

Follow the on-screen prompts to select student cases and view depression risk predictions.

## Features

- **Data Validation**: Validates input data to ensure it meets required format
- **Data Visualization**: Generates visualizations of key factors affecting depression risk
- **Machine Learning Model**: Uses Random Forest classifier to predict depression probability
- **Feature Importance Analysis**: Identifies key factors contributing to depression risk
- **Case Management**: Pre-defined student profiles for easy evaluation
- **Risk Assessment**: Provides depression risk level and recommendations

## Core Components

- **DataValidator**: Validates user input data against expected formats and ranges
- **StudentDepressionPredictor**: Core prediction engine that trains the model and makes predictions
- **StudentCaseManager**: Manages pre-defined student cases for assessment

## Output

The program generates:
- Predictive analysis with risk levels (LOW, MEDIUM, HIGH)
- Recommendations based on risk level
- Visual analysis of data (saved in the `images` directory)
- Feature importance ranking