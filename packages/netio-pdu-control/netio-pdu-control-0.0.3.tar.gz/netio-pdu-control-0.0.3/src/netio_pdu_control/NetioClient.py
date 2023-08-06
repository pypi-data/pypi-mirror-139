from requests.auth import HTTPBasicAuth
import requests
import urllib.parse


class Client:
    def __init__(self, read_login, write_login, address) -> None:
        self.read_auth = HTTPBasicAuth(read_login[0], read_login[1])
        self.write_auth = HTTPBasicAuth(write_login[0], write_login[1])
        self.url = urllib.parse.urljoin(address, "netio.json")

    def status(self):
        response = requests.get(self.url, auth=self.read_auth)
        return response.json()

    def set(self, json):
        response = requests.post(self.url, auth=self.write_auth, json=json)
        return response.json()

    def set_power(self, outlet: int, state: bool):
        args = {
            "Outputs": [{
                "ID": outlet,
                "Action": int(state)
            }]
        }
        return self.set(args)

    def set_power_period(self, outlet: int, state: bool, delay: int = 5000):
        args = {
            "Outputs": [{
                "ID": outlet,
                "Action": 3 if state else 2,
                "Delay": delay
            }]
        }
        return self.set(args)

    def toggle_power(self, outlet: int):
        args = {
            "Outputs": [{
                "ID": outlet,
                "Action": 4
            }]
        }
        return self.set(args)
