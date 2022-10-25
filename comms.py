import requests


class http_handler:
    _payload = ""


    def __init__(self:object, site:int):
        self._endpoint = "localhost:3000/anpr/"+site

    def post_b_64(self:object, b:str) -> None:
        pass
