import modified_view


def handle_signup(self):
    username_entry = self.username_entry.input()
    password_entry = self.password_entry.input()


def validate_credentials( username_entry, password_entry):
    """
    Validates the username and password against a .txt file.
    Each line in the file should have the format: username,password
    """
    try:
        with open("credentials.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username_entry == stored_username and password_entry == stored_password:
                    return True
    except FileNotFoundError:
        print("Error: credentials.txt file not found.")
    return False