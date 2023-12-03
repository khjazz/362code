from validation import is_valid_user_info


class User:
    """
    This class contains the logic to validate data for user login.
    """

    def login(data):
        """
        Return True if the user info is valid, False otherwise.
        """
        if "username" not in data or "password" not in data:
            return False
        username, password = data["username"], data["password"]
        return is_valid_user_info(username, password)
