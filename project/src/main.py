import logging
import os
from time import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from flask import Flask, request
from validation import is_valid_simulations, is_valid_concurrency, is_valid_protocol
from pi_estimator import estimate_pi_processes
from login_stat import LoginStat
from quote_client import get_quotes
from user import User

app = Flask(__name__)
STAT_FILENAME = "login_stat.json"
SERVER_LOG = "serverinfo.log"
QUOTE_SERVER_HOST, QUOTE_SERVER_PORT = "localhost", 1700


def handle_login(data):
    """
    Handle login with user data. Return True if login is successful, False otherwise.
    """
    if User.login(data):
        logging.info(f"User-{data['username']} logged in from {request.remote_addr}")
        login_stat.increment_user_login_count(data["username"])
        return True
    else:
        logging.info(
            f"Failed login attempt from {request.remote_addr} to user-{data.get('username', 'unknown')} "
        )
        return False


def validate_request(data, required_fields, optional_fields):
    """
    Validate request data.
    Return error message and status code if validation fails, None otherwise.
    Takes in the data, a dictionary of required fields and their validators,
    and a dictionary of optional fields and their validators.
    """
    # check if the request contains all required fields
    # and if the fields are valid
    # if not, return error message and status code
    for field, validator in required_fields.items():
        if field not in data:
            return {"error": f"missing field {field}"}, 400
        if not validator(data[field]):
            return {"error": f"invalid field {field}"}, 400

    # check if the optional fields are valid
    # if not, return error message and status code
    for field, validator in optional_fields.items():
        if field in data and not validator(data[field]):
            return {"error": f"invalid field {field}"}, 400

    return None, None


@app.post("/pi")
def pi():
    start_time = time()
    data = request.get_json()

    logging.debug("Received data: " + str(data) + " from " + request.remote_addr)
    if not handle_login(data):
        return {"error": "user info error"}, 401

    error, status = validate_request(
        data,
        {"simulations": is_valid_simulations},
        {"concurrency": is_valid_concurrency},
    )

    if error:
        logging.info(f"invalid request from {request.remote_addr} error: {error}")
        return error, status

    result = estimate_pi_processes(
        data["simulations"], data.get("concurrency", 1), pi_executor
    )
    # add time value into the return dictionary
    result["time"] = time() - start_time
    logging.debug(result)
    return result


@app.post("/quote")
def quote():
    start_time = time()
    data = request.get_json()

    logging.debug("Received data: " + str(data) + " from " + request.remote_addr)
    if not handle_login(data):
        return {"error": "user info error"}, 401

    error, status = validate_request(
        data, {"protocol": is_valid_protocol}, {"concurrency": is_valid_concurrency}
    )

    if error:
        logging.info(f"invalid request from {request.remote_addr} error: {error}")
        return error, status

    result = get_quotes(
        QUOTE_SERVER_HOST,
        QUOTE_SERVER_PORT,
        data["protocol"],
        data.get("concurrency", 1),
        quote_executor,
    )
    # add time value into the return dictionary
    result["time"] = time() - start_time
    logging.debug(result)
    return result


if __name__ == "__main__":
    if os.environ.get("PROD"):
        logging.basicConfig(level=logging.INFO, filename=SERVER_LOG)
    else:
        logging.basicConfig(level=logging.DEBUG)
    login_stat = LoginStat(STAT_FILENAME)
    with ProcessPoolExecutor() as pi_executor, ThreadPoolExecutor() as quote_executor:
        app.run()
