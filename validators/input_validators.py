
class InputValidator:
    
    @staticmethod
    def validate_int_input(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            else:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def validate_numeric_string(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return value  
            else:
                print("Invalid input. Please enter digits only.")

    @staticmethod
    def validate_int_input_update(prompt):        
        while True:
            value = input(prompt).strip()
            if value == "":
                break
            if value.isdigit():
                return int(value)
            else:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def validate_numeric_string_update(prompt):
        while True:
            value = input(prompt).strip()
            if value == "":
                break
            if value.isdigit():
                return value
            else:
                print("Invalid input. Please enter digits only.")

    @staticmethod
    def validate_alpha_string(prompt):
        while True:
            value = input(prompt).strip()
            if all(part.isalpha() for part in value.split()):
                return value
            else:
                print("Invalid input. Please enter letters only (first and last name allowed).")


    @staticmethod
    def validate_alpha_string_update(prompt):
        while True:
            value = input(prompt).strip()
            if value == "":
                return None
            if all(part.isalpha() for part in value.split()):
                return value
            else:
                print("Invalid input. Please enter letters only (first and last name allowed).")


    @staticmethod
    def choose_option(prompt, valid_options):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in [opt.lower() for opt in valid_options]:
                return user_input
            else:
                print("Please choose a valid option!")

    @staticmethod
    def choose_option_withSkip(prompt, valid_options):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input == "":
                return None
            if user_input in [opt.lower() for opt in valid_options]:
                return user_input
            else:
                print("Please choose a valid option!")