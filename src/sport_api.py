import http.client

class SportAPI:
    def __init__(self, name:str, api_url: str, service: str) -> None:
        self.name = name
        self.url = api_url
        self.service = service

class APIConnection:
    def __init__(self, api_url: str, service: str) -> None:
        self.url = api_url
        self.service = service

    def connect(self) -> str:
        # TODO : Call an API to get the result of the fight
        conn = http.client.HTTPSConnection(self.url)
        conn.request("GET",self.service)
        res = conn.getresponse()
        data = res.read()
        return (data.decode("utf-8"))
