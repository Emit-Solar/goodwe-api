import requests
import json
from typing import Dict, Any, List, Tuple


class GoodWeClient:
    def __init__(self, username, pwd, base_url, default_headers, log):
        """
        Args:
            username (str): GoodWe account username.
            pwd (str): GoodWe account password.
            base_url (str): Base URL of the GoodWe API.
            default_headers (Dict[str, str]): Default headers.
            log (Any): Logger instance.
        """
        self.username = username
        self.pwd = pwd
        self.token = ""
        self.logged_in = False

        self.base_url = base_url
        self.default_headers = default_headers
        self.log = log

        self.log.info("GoodWeClient initialized")
        self.login()

    def send_request(
        self, endpoint, headers, version="v3", data=None, method="POST"
    ) -> Dict[str, Any]:
        """
        Sends a request to the GoodWe API.
        Args:
            endpoint (str): API endpoint path.
            headers (Dict[str, str]): Headers for the request.
            version (str): API version (v2/v3).
            data (Optional[Dict[str, Any]]): JSON data to send with request.
            method (str): HTTP method, either "POST" or "GET".

        Returns:
            JSON response from the API (Dict[str, Any]).
        """
        try:
            if not self.logged_in and endpoint != "/Common/CrossLogin":
                raise Exception("User not logged in")

            url = f"{self.base_url}{version}{endpoint}"

            if method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "GET":
                response = requests.get(url, headers=headers, json=data)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()

            response = response.json()
            if response["msg"] in ["success", "Successful"]:
                return response
            else:
                raise Exception(response["msg"])

        except Exception as e:
            self.log.exception(f"{version}{endpoint} request failed.", e)
            raise e

    def login(self):
        """
        Retrieves and stores API token.
        """
        self.log.info("Logging in to GoodWe API")
        url = "/Common/CrossLogin"
        headers = {
            "token": json.dumps(
                {
                    "uid": "",
                    "timestamp": 0,
                    "token": "",
                    "client": "web",
                    "version": "",
                    "language": "en-US",
                }
            )
        }
        data = {"account": self.username, "pwd": self.pwd, "is_local": False}

        try:
            response = self.send_request(url, headers, data=data)
            self.token = json.dumps(response["data"])
            self.logged_in = True
            self.log.info("Login successful")
        except Exception as e:
            self.log.exception("Login failed", e)
            raise e

    def get_plant_list(self) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Retreives basic information about all plants. (v2)
        Returns:
            Number of plants (int)
            List of dicts containing plant information (List[Dict[str, Any]])
                - plantId (str)
                - plantName (str)
                - hasInverters (int)
                - classification (str)
                - plantTypes : unknown
                - capacity (str) : kW
                - batteryCapacity : unknown
                - createDate (str) : MM/DD/YYYY
                - latitude (str)
                - longitude (str)

        """
        self.log.info("Getting plant list")
        endpoint = "/PlantManage/GetPlantList"
        data = {
            "pager": {
                "data": {},
            }
        }

        headers = self.default_headers.copy()
        headers["token"] = self.token

        try:
            response = self.send_request(endpoint, headers, version="v2", data=data)
            self.log.info("Plant list retrieved successfully")
            plant_num = response["data"]["page"]["records"]
            return plant_num, response["data"]["rows"]
        except Exception as e:
            self.log.exception("Failed to get plant list", e)
            raise e
