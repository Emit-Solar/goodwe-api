import requests
import json


class GoodWeClient:
    def __init__(self, username, pwd, base_url, default_headers):
        self.username = username
        self.pwd = pwd
        self.token = ""
        self.logged_in = False

        self.base_url = base_url
        self.default_headers = default_headers

    # Sends request to the GoodWe API
    def send_request(self, endpoint, headers, data=None, method="POST"):
        try:
            # Requests aside from CrossLogin require authentication
            if not self.logged_in and endpoint != "/Common/CrossLogin":
                raise Exception("User not logged in")

            url = f"{self.base_url}{endpoint}"
            headers = headers | self.default_headers

            if method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "GET":
                response = requests.get(url, headers=headers, json=data)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()  # HTTPError

            return response.json()
        except Exception as e:
            raise Exception(f"API error: {e}") from e

    # Authentication to obtain token
    def login(self):
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

        response = self.send_request(url, headers, data=data)

        if response["msg"] == "Successful":
            self.token = response["data"]["token"]
            self.logged_in = True
            return
        else:
            raise Exception(response["msg"])
