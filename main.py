from src.student_case_manager import StudentCaseManager
from src.depression_predictor import StudentDepressionPredictor
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)


def display_prediction_results(predictor, student_case, case_number):
    """
    Display prediction results in console

    Args:
        predictor: Trained depression prediction model
        student_case (dict): Student case data
        case_number (int): Number of the selected case
    """
    try:
        # Predict depression risk, passing the case number
        predictor.predict_depression(student_case, case_number)

    except Exception as e:
        print(f"Prediction Error: {e}")


def main():
    """
    Main entry point for the Student Depression Predictor application
    """
    # Determine the path to the dataset
    dataset_path = os.path.join(
        project_root, 'data', 'student_depression_dataset.csv')

    try:
        # Create an instance of the predictor
        predictor = StudentDepressionPredictor(dataset_path)

        # Create a student case manager
        case_manager = StudentCaseManager()

        while True:
            # Display available student cases
            cases = case_manager.list_student_cases()
            print("\n=== STUDENT DEPRESSION RISK PREDICTOR ===")
            print("Available Student Cases:")
            for case in cases:
                print(f"Case {case['Index']}: "
                      f"Gender: {case['Gender']}, "
                      f"Age: {case['Age']}, "
                      f"Degree: {case['Degree']}")

            # Prompt user to select a case
            print("\nEnter the case number you want to evaluate (or 0 to exit):")
            try:
                case_index = int(input("Case number: "))

                # Exit condition
                if case_index == 0:
                    print("Exiting the program. Goodbye!")
                    break

                # Get selected student case
                student_case = case_manager.get_student_case(case_index)

                if student_case:
                    # Display prediction results, passing the case index
                    display_prediction_results(
                        predictor, student_case, case_index)

                # Ask if user wants to continue
                continue_choice = input(
                    "\nDo you want to evaluate another case? (yes/no): ").lower()
                if continue_choice != 'yes':
                    print("Exiting the program. Goodbye!")
                    break

            except ValueError:
                print("Invalid input. Please enter a valid case number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    except FileNotFoundError:
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please ensure the dataset is placed in the 'data' directory.")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
