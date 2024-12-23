from typing import Dict
from typing import List
from typing import Optional

import requests
from pydantic import BaseModel
from pydantic import Extra
from urllib.parse import urlencode
from urllib.parse import urljoin

from openai.types.chat import ChatCompletion

BASE_URL = "https://api.galadriel.com"


class GaladrielChatHistory(BaseModel):
    request: Dict
    response: ChatCompletion
    hash: str
    public_key: str
    signature: str
    attestation: str
    tx_hash: str


class ExtendedChatCompletion(ChatCompletion):
    class Config:
        extra = Extra.allow  # This will allow extra attributes to be stored


class GaladrielError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"Error: {self.msg}"


def get_history(
    galadriel_api_key: str, limit: int = 10, cursor: str = None, filter: str = "all"
) -> List[GaladrielChatHistory]:
    if filter not in ["all", "mine"]:
        raise GaladrielError("Incorrect filter given, valid values are: 'all', 'mine'")

    query_params = {"limit": limit, "filter": filter}
    if cursor:
        query_params["cursor"] = cursor

    return _make_request(galadriel_api_key, query_params)


def get_by_hash(galadriel_api_key: str, hash: str) -> Optional[GaladrielChatHistory]:
    try:
        url = urljoin(BASE_URL, f"/v1/verified/chat/completions/{hash}")
        headers = {"accept": "application/json", "Authorization": galadriel_api_key}
        response = requests.get(url, headers=headers)
        response_data = response.json()
        return _map_one(response_data)
    except:
        return None


def _make_request(
    galadriel_api_key: str, query_params: Optional[Dict]
) -> List[GaladrielChatHistory]:
    try:
        url = urljoin(BASE_URL, "/v1/verified/chat/completions")

        if query_params:
            encoded_params = urlencode(query_params)
            url = url + f"?{encoded_params}"

        print("url:", url)
        headers = {"accept": "application/json", "Authorization": galadriel_api_key}
        response = requests.get(url, headers=headers)
        response_data = response.json()
        return _map_list(response_data)
    except:
        return []


def _map_list(response_data) -> List[ChatCompletion]:
    result = []
    for completion_data in response_data.get("completions"):
        item = _map_one(completion_data)
        result.append(item)
    return result


def _map_one(completion_data: Dict) -> ChatCompletion:
    response = ChatCompletion.parse_obj(
        completion_data.get("response"),
    )
    return GaladrielChatHistory(
        request=completion_data.get("request"),
        response=response,
        hash=completion_data.get("hash"),
        public_key=completion_data.get("public_key"),
        signature=completion_data.get("signature"),
        attestation=completion_data.get("attestation"),
        tx_hash=completion_data.get("tx_hash"),
    )
