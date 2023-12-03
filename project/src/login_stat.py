import json
import threading


class LoginStat:
    """
    Keep track of the number of times a user has logged in.
    """

    def __init__(self, filename):
        """
        Set the filename and initialize the lock and log attributes.
        """
        self.filename = filename
        self.lock = threading.Lock()
        self.log = self.load()

    def load(self):
        """
        Load user login count from json file.
        """
        with self.lock:
            try:
                with open(self.filename) as file:
                    return json.load(file)
            except FileNotFoundError:
                return {}

    def increment_user_login_count(self, username, increment=1):
        """
        increment the login count for the user.
        Set to 1 if the user is not in the log.
        """
        with self.lock:
            self.log[username] = self.log.get(username, 0) + increment
            with open(self.filename, "w") as file:
                json.dump(self.log, file)
