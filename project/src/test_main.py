import unittest
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from math import pi as PI
from main import STAT_FILENAME

SERVER = "localhost:5000"


def ws_client(url, method=None, data=None):
    if not method:
        method = "POST" if data else "GET"
    if data:
        data = json.dumps(data).encode()
    headers = {"Content-type": "application/json; charset=UTF-8"} if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result


class TestLoginValidation(unittest.TestCase):
    """
    Test for the login validation logic.
    """

    def setUp(self):
        self.endpoints = ["pi", "quote"]
        self.invalid_usernames = ["", "a123", "12345", ":)"]
        self.invalid_passwords_suffix = ["", "pw", "--pw", " pw"]

    def server_login(self, endpoint, username=None, password=None, server=SERVER):
        """
        Helper function to login to the server.
        """
        info = {}
        if username is not None:
            info["username"] = username
        if password is not None:
            info["password"] = password
        ws_client(f"http://{server}/{endpoint}", "POST", info)

    def test_valid_user_info(self):
        """
        Test with valid user info.
        Should not have "user info error" and status code 401 in the response.
        """
        for endpoint in self.endpoints:
            try:
                self.server_login(endpoint, username="0000", password="0000-pw")
            except HTTPError as e:
                self.assertNotEqual(401, e.code)
                self.assertNotEqual(
                    "user info error", json.loads(e.read().decode())["error"]
                )

    def test_missing_username(self):
        """
        Test with missing username.
        Should have "user info error" and status code 401 in the response.
        """
        for endpoint in self.endpoints:
            self.assert_login_error(endpoint, password="0000-pw")

    def test_missing_password(self):
        """
        Test with missing password.
        Should have "user info error" and status code 401 in the response.
        """
        for endpoint in self.endpoints:
            self.assert_login_error(endpoint, username="0000")

    def test_invalid_username_format(self):
        """
        Test with invalid username formats.
        Should have "user info error" and status code 401 in the response.
        """
        for endpoint in self.endpoints:
            for username in self.invalid_usernames:
                self.assert_login_error(
                    endpoint, username=username, password=username + "-pw"
                )

    def test_invalid_password_format(self):
        """
        Test with invalid password formats.
        Should have "user info error" and status code 401 in the response."""
        username = "0000"
        for endpoint in self.endpoints:
            for password_suffix in self.invalid_passwords_suffix:
                self.assert_login_error(
                    endpoint, username=username, password=username + password_suffix
                )

    def assert_login_error(self, endpoint, username=None, password=None):
        """
        Helper function to assert login error.
        """
        with self.assertRaises(HTTPError) as cm:
            self.server_login(endpoint, username=username, password=password)
        self.assertEqual(401, cm.exception.code)
        self.assertEqual(
            "user info error", json.loads(cm.exception.read().decode())["error"]
        )


class TestLoginStat(TestLoginValidation):
    """
    Test for the login statistics functionality.
    """

    def get_login_count(self, username):
        """
        Helper function to get the login count of a user.
        """
        try:
            with open(STAT_FILENAME) as file:
                log = json.load(file)
        except:
            log = {}
        return log.get(username, 0)

    def assert_count_diff_with_login(self, endpoint, username, password, count_diff):
        """
        Helper function to assert the login count difference after login.
        """
        login_count_before = self.get_login_count(username)
        try:
            self.server_login(endpoint, username=username, password=password)
        except HTTPError:
            pass
        login_count_after = self.get_login_count(username)
        self.assertEqual(login_count_before + count_diff, login_count_after)

    def test_login_stat(self):
        """
        Test the login statistics with valid user info.
        Should increase the login count by 1 for each login.
        """
        for endpoint in self.endpoints:
            self.assert_count_diff_with_login(endpoint, "0000", "0000-pw", 1)

    def test_login_stat_with_invalid_user_info(self):
        """
        Test the login statistics with invalid user info.
        Should not increase the login count.
        """
        for endpoint in self.endpoints:
            self.assert_count_diff_with_login(endpoint, "0000", "0000", 0)

    def test_login_stat_concurrency(self):
        """
        Test the login statistics with concurrency.
        Should increase the login count by the number of concurrency.
        """
        for endpoint in self.endpoints:
            login_count_before = self.get_login_count("0000")
            with ThreadPoolExecutor() as executor:
                try:
                    executor.map(
                        self.server_login,
                        [endpoint] * 20,
                        ["0000"] * 20,
                        ["0000-pw"] * 20,
                    )
                except HTTPError:
                    pass
            login_count_after = self.get_login_count("0000")
            self.assertEqual(login_count_before + 20, login_count_after)


class BaseTestWebService(unittest.TestCase):
    INVALID_SIMULATIONS = [99, 100000001, "100", 100.0, None]
    INVALID_PROTOCOL = [1, "http", "smtp", None]
    INVALID_CONCURRENCIES = [0, 9, -100, None]

    def assert_ws_error(self, request, data, expect_code, expected_error):
        """
        Helper function to assert the error response of a web service.
        """
        with self.assertRaises(HTTPError) as cm:
            request(data)
        self.assertEqual(expect_code, cm.exception.code)
        self.assertEqual(
            expected_error, json.loads(cm.exception.read().decode())["error"]
        )


class TestPiEndpoint(BaseTestWebService):
    def pi_ws(self, data):
        """
        Helper function to call the pi estimation web service.
        """
        return ws_client(f"http://{SERVER}/pi", "POST", data)

    def test_estimate_pi(self):
        """
        Test with valid user info.
        Should return the estimated pi value within 1 of the actual value.
        """
        data = {"username": "9999", "password": "9999-pw", "simulations": 100}
        pi_resp = self.pi_ws(data)
        epsilon = 1
        self.assertTrue("pi" in pi_resp)
        self.assertTrue(abs(pi_resp["pi"] - PI) < epsilon)

    def test_pi_processing_time_vs_concurrency(self):
        """
        Test the processing time of the pi estimation web service with different concurrency.
        Should have the processing time decrease as the concurrency increases.
        """
        simulations = 1000000
        data_one_concurrency = {
            "username": "9999",
            "password": "9999-pw",
            "simulations": simulations,
        }
        data_eight_concurrency = {
            "username": "9999",
            "password": "9999-pw",
            "simulations": simulations,
            "concurrency": 8,
        }
        # warm up the server
        self.pi_ws(data_eight_concurrency)

        time_one_concurrency = self.pi_ws(data_one_concurrency).get("time")
        time_eight_concurrency = self.pi_ws(data_eight_concurrency).get("time")
        self.assertLess(time_eight_concurrency, time_one_concurrency)

    def test_pi_accuracy_vs_simulations(self):
        """Test the accuracy of the pi estimation web service with different number of simulations.
        Should have the accuracy increase as the number of simulations increases.
        """
        data_1000_simulations = {
            "username": "9999",
            "password": "9999-pw",
            "simulations": 1000,
        }
        data_100000_simulations = {
            "username": "9999",
            "password": "9999-pw",
            "simulations": 100000,
        }
        error_1000_simulations = abs(self.pi_ws(data_1000_simulations).get("pi") - PI)
        error_100000_simulations = abs(
            self.pi_ws(data_100000_simulations).get("pi") - PI
        )
        self.assertLess(error_100000_simulations, error_1000_simulations)

    def test_pi_simulations_distribution_with_prime_number(self):
        """
        Test with a (somewhat) large prime number to make sure the distribution numbers are correct.
        As a prime number is indivisible except by itself and 1,
        which is a good edge case to test the partition function,
        when the number of simulations is indivisible by the number of concurrency.
        """
        large_prime_number = 7919
        for i in range(1, 9):
            data = {
                "username": "9999",
                "password": "9999-pw",
                "simulations": large_prime_number,
                "concurrency": i,
            }
            pi_resp = self.pi_ws(data)
            self.assertEqual(
                large_prime_number, sum(pi_resp["simulations_distribution"])
            )

    def test_pi_missing_simulations_key(self):
        """
        Test with missing simulations key.
        Should have "missing field simulations" and status code 400 in the response."""
        data = {"username": "9999", "password": "9999-pw", "concurrency": 1}
        self.assert_ws_error(self.pi_ws, data, 400, "missing field simulations")

    def test_pi_invalid_simulations(self):
        """
        Test with invalid simulations.
        Should have "invalid field simulations" and status code 400 in the response."""
        for simulations in self.INVALID_SIMULATIONS:
            data = {
                "username": "9999",
                "password": "9999-pw",
                "simulations": simulations,
                "concurrency": 1,
            }
            self.assert_ws_error(self.pi_ws, data, 400, "invalid field simulations")

    def test_pi_default_concurrency(self):
        """
        Test without supplying concurrency.
        Should have the default concurrency 1.
        """
        data = {"username": "9999", "password": "9999-pw", "simulations": 100}
        pi_resp = self.pi_ws(data)
        self.assertEqual(1, pi_resp["concurrency"])

    def test_pi_invalid_concurrency(self):
        """
        Test with invalid concurrency.
        Should have "invalid field concurrency" and status code 400 in the response.
        """
        for concurrency in self.INVALID_CONCURRENCIES:
            data = {
                "username": "9999",
                "password": "9999-pw",
                "simulations": 100,
                "concurrency": concurrency,
            }
            self.assert_ws_error(self.pi_ws, data, 400, "invalid field concurrency")


class TestQuoteEndpoint(BaseTestWebService):
    def quote_ws(self, data):
        """Helper function to call the quote web service."""
        return ws_client(f"http://{SERVER}/quote", "POST", data)

    def test_get_quotes_with_tcp(self):
        """
        Test with different concurrency.
        The returned quotes should be the same as the number of concurrency.
        And the protocol should be tcp.
        """
        for i in range(1, 9):
            data = {
                "username": "9998",
                "password": "9998-pw",
                "protocol": "tcp",
                "concurrency": i,
            }
            quote_resp = self.quote_ws(data)
            self.assertEqual(i, len(quote_resp["quotes"]))
            self.assertEqual("tcp", quote_resp["protocol"])

    def test_get_quotes_with_udp(self):
        """
        Test with different concurrency.
        The returned quotes should be the same as the number of concurrency.
        And the protocol should be udp.
        """
        for i in range(1, 9):
            data = {
                "username": "9998",
                "password": "9998-pw",
                "protocol": "udp",
                "concurrency": i,
            }
            quote_resp = self.quote_ws(data)
            self.assertEqual(i, len(quote_resp["quotes"]))
            self.assertEqual("udp", quote_resp["protocol"])

    def test_quote_missing_protocol_key(self):
        """
        Test with missing protocol key.
        Should have "missing field protocol" and status code 400 in the response.
        """
        data = {"username": "9998", "password": "9998-pw", "concurrency": 1}
        with self.assertRaises(HTTPError) as cm:
            self.quote_ws(data)
        self.assertEqual(400, cm.exception.code)
        self.assertEqual(
            "missing field protocol", json.loads(cm.exception.read().decode())["error"]
        )

    def test_quote_invalid_protocol(self):
        """Test with invalid protocol.
        Should have "invalid field protocol" and status code 400 in the response.
        """
        for protocol in self.INVALID_PROTOCOL:
            data = {
                "username": "9998",
                "password": "9998-pw",
                "protocol": protocol,
                "concurrency": 1,
            }
            self.assert_ws_error(self.quote_ws, data, 400, "invalid field protocol")

    def test_quote_default_concurrency(self):
        """Test without supplying concurrency.
        Should have the default concurrency 1."""
        data = {"username": "9998", "password": "9998-pw", "protocol": "tcp"}
        quote_resp = self.quote_ws(data)
        self.assertEqual(1, quote_resp["concurrency"])

    def test_quote_invalid_concurrency(self):
        """Test with invalid concurrency.
        Should have "invalid field concurrency" and status code 400 in the response.
        """
        for concurrency in self.INVALID_CONCURRENCIES:
            data = {
                "username": "9998",
                "password": "9998-pw",
                "protocol": "tcp",
                "concurrency": concurrency,
            }
            self.assert_ws_error(self.quote_ws, data, 400, "invalid field concurrency")


if __name__ == "__main__":
    unittest.main()
