import re


USERNAME_REGEX = r"^[0-9]{4}$"


def is_valid_user_info(username, password):
    """
    Return True if username and password are valid, False otherwise.
    """
    if not isinstance(username, str) or not re.match(USERNAME_REGEX, username):
        return False
    if not isinstance(password, str) or password != username + "-pw":
        return False
    return True


def is_valid_concurrency(concurrency):
    """
    Return True if concurrency is between 1 and 8, False otherwise.
    """
    return isinstance(concurrency, int) and 1 <= concurrency <= 8


def is_valid_simulations(simulations):
    """
    Return True if simulations is between 100 and 100000000, False otherwise.
    """
    return isinstance(simulations, int) and 100 <= simulations <= 100000000


def is_valid_protocol(protocol):
    """
    Return True if protocol is "tcp" or "udp" , False otherwise.
    """
    return isinstance(protocol, str) and protocol in ["tcp", "udp"]
