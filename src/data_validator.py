import re


class DataValidator:

    @staticmethod
    def validate_gender(gender):

        valid_genders = ['Male', 'Female', 'Other']
        return gender.capitalize() if gender.capitalize() in valid_genders else None

    @staticmethod
    def validate_age(age):

        try:
            age = int(age)
            return age if 15 <= age <= 35 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_profession(profession):

        valid_professions = ['Student']
        return profession.capitalize() if profession.capitalize() in valid_professions else None

    @staticmethod
    def validate_academic_pressure(pressure):

        try:
            pressure = int(pressure)
            return pressure if 1 <= pressure <= 10 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_cgpa(cgpa):

        try:
            cgpa = float(cgpa)
            return cgpa if 0 <= cgpa <= 4.0 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_study_satisfaction(satisfaction):

        try:
            satisfaction = int(satisfaction)
            return satisfaction if 1 <= satisfaction <= 10 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_sleep_duration(duration):

        valid_durations = ['Less than 6 hours',
                           '6-8 hours', 'More than 8 hours']
        return duration if duration in valid_durations else None

    @staticmethod
    def validate_dietary_habits(habits):

        valid_habits = ['Healthy', 'Unhealthy', 'Average']
        return habits.capitalize() if habits.capitalize() in valid_habits else None

    @staticmethod
    def validate_degree(degree):

        valid_degrees = ['Bachelors', 'Masters', 'PhD']
        return degree.capitalize() if degree.capitalize() in valid_degrees else None

    @staticmethod
    def validate_suicidal_thoughts(thoughts):

        valid_responses = ['Yes', 'No']
        return thoughts.capitalize() if thoughts.capitalize() in valid_responses else None

    @staticmethod
    def validate_work_study_hours(hours):

        try:
            hours = int(hours)
            return hours if 0 <= hours <= 24 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_financial_stress(stress):

        try:
            stress = int(stress)
            return stress if 1 <= stress <= 10 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_family_history(history):

        valid_responses = ['Yes', 'No']
        return history.capitalize() if history.capitalize() in valid_responses else None

    def validate_input(self, input_data):

        validated_data = {}
        validation_methods = {
            'Gender': self.validate_gender,
            'Age': self.validate_age,
            'Profession': self.validate_profession,
            'Academic Pressure': self.validate_academic_pressure,
            'CGPA': self.validate_cgpa,
            'Study Satisfaction': self.validate_study_satisfaction,
            'Sleep Duration': self.validate_sleep_duration,
            'Dietary Habits': self.validate_dietary_habits,
            'Degree': self.validate_degree,
            'Have you ever had suicidal thoughts ?': self.validate_suicidal_thoughts,
            'Work/Study Hours': self.validate_work_study_hours,
            'Financial Stress': self.validate_financial_stress,
            'Family History of Mental Illness': self.validate_family_history
        }

        # Validate each input
        for key, value in input_data.items():
            if key in validation_methods:
                validated_value = validation_methods[key](value)
                if validated_value is None:
                    print(f"Invalid input for {key}: {value}")
                    return None
                validated_data[key] = validated_value
            else:
                print(f"Unexpected input field: {key}")
                return None

        # Ensure all required fields are present
        required_fields = set(validation_methods.keys())
        input_fields = set(input_data.keys())

        if not required_fields.issubset(input_fields):
            missing_fields = required_fields - input_fields
            print(f"Missing required fields: {missing_fields}")
            return None

        return validated_data
