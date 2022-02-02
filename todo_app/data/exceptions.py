from typing import Dict


class ResponseError(Exception):
    def __init__(self, json: Dict):
        self.json = json
