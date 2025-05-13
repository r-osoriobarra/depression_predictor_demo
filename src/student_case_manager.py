class StudentCaseManager:
    # student cases
    def __init__(self):

        self.student_cases = [
            {
                'Gender': 'Female',
                'Age': 22,
                'Profession': 'Student',
                'Academic Pressure': 8,
                'CGPA': 3.5,
                'Study Satisfaction': 6,
                'Sleep Duration': '6-8 hours',
                'Dietary Habits': 'Healthy',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'No',
                'Work/Study Hours': 6,
                'Financial Stress': 5,
                'Family History of Mental Illness': 'No'
            },
            {
                'Gender': 'Male',
                'Age': 20,
                'Profession': 'Student',
                'Academic Pressure': 9,
                'CGPA': 3.2,
                'Study Satisfaction': 4,
                'Sleep Duration': 'Less than 6 hours',
                'Dietary Habits': 'Unhealthy',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'Yes',
                'Work/Study Hours': 8,
                'Financial Stress': 8,
                'Family History of Mental Illness': 'Yes'
            },
            {
                'Gender': 'Female',
                'Age': 25,
                'Profession': 'Student',
                'Academic Pressure': 7,
                'CGPA': 3.8,
                'Study Satisfaction': 7,
                'Sleep Duration': '6-8 hours',
                'Dietary Habits': 'Healthy',
                'Degree': 'Masters',
                'Have you ever had suicidal thoughts ?': 'No',
                'Work/Study Hours': 5,
                'Financial Stress': 4,
                'Family History of Mental Illness': 'No'
            },
            {
                'Gender': 'Male',
                'Age': 23,
                'Profession': 'Student',
                'Academic Pressure': 6,
                'CGPA': 3.0,
                'Study Satisfaction': 5,
                'Sleep Duration': 'More than 8 hours',
                'Dietary Habits': 'Average',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'No',
                'Work/Study Hours': 7,
                'Financial Stress': 6,
                'Family History of Mental Illness': 'Yes'
            },
            {
                'Gender': 'Female',
                'Age': 21,
                'Profession': 'Student',
                'Academic Pressure': 9,
                'CGPA': 3.9,
                'Study Satisfaction': 3,
                'Sleep Duration': 'Less than 6 hours',
                'Dietary Habits': 'Unhealthy',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'Yes',
                'Work/Study Hours': 9,
                'Financial Stress': 7,
                'Family History of Mental Illness': 'No'
            },
            {
                'Gender': 'Male',
                'Age': 24,
                'Profession': 'Student',
                'Academic Pressure': 5,
                'CGPA': 2.8,
                'Study Satisfaction': 4,
                'Sleep Duration': '6-8 hours',
                'Dietary Habits': 'Unhealthy',
                'Degree': 'Masters',
                'Have you ever had suicidal thoughts ?': 'Yes',
                'Work/Study Hours': 6,
                'Financial Stress': 9,
                'Family History of Mental Illness': 'Yes'
            },
            {
                'Gender': 'Female',
                'Age': 19,
                'Profession': 'Student',
                'Academic Pressure': 7,
                'CGPA': 3.6,
                'Study Satisfaction': 6,
                'Sleep Duration': '6-8 hours',
                'Dietary Habits': 'Healthy',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'No',
                'Work/Study Hours': 5,
                'Financial Stress': 3,
                'Family History of Mental Illness': 'No'
            },
            {
                'Gender': 'Male',
                'Age': 26,
                'Profession': 'Student',
                'Academic Pressure': 8,
                'CGPA': 3.3,
                'Study Satisfaction': 5,
                'Sleep Duration': 'Less than 6 hours',
                'Dietary Habits': 'Average',
                'Degree': 'PhD',
                'Have you ever had suicidal thoughts ?': 'Yes',
                'Work/Study Hours': 8,
                'Financial Stress': 6,
                'Family History of Mental Illness': 'Yes'
            },
            {
                'Gender': 'Female',
                'Age': 22,
                'Profession': 'Student',
                'Academic Pressure': 6,
                'CGPA': 3.7,
                'Study Satisfaction': 7,
                'Sleep Duration': 'More than 8 hours',
                'Dietary Habits': 'Healthy',
                'Degree': 'Masters',
                'Have you ever had suicidal thoughts ?': 'No',
                'Work/Study Hours': 4,
                'Financial Stress': 4,
                'Family History of Mental Illness': 'No'
            },
            {
                'Gender': 'Male',
                'Age': 20,
                'Profession': 'Student',
                'Academic Pressure': 9,
                'CGPA': 2.5,
                'Study Satisfaction': 3,
                'Sleep Duration': 'Less than 6 hours',
                'Dietary Habits': 'Unhealthy',
                'Degree': 'Bachelors',
                'Have you ever had suicidal thoughts ?': 'Yes',
                'Work/Study Hours': 7,
                'Financial Stress': 8,
                'Family History of Mental Illness': 'Yes'
            }
        ]

    def list_student_cases(self):

        case_details = []
        for i, case in enumerate(self.student_cases, 1):
            case_details.append({
                'Index': i,
                'Gender': case['Gender'],
                'Age': case['Age'],
                'Degree': case['Degree']
            })
        return case_details

    def get_student_case(self, index):

        try:
            return self.student_cases[index - 1]
        except IndexError:
            print(
                f"Invalid case index. Please choose between 1 and {len(self.student_cases)}")
            return None
