from typing import Any

from fastel.config import SdkConfig
from fastel.payment.ecpay.models.map import CvsMapRequestModel
from fastel.utils import requests


def cvs_map_request(data: CvsMapRequestModel) -> Any:
    url = f"{SdkConfig.payment_host}/ecpay/logistics/map/request?client_id={SdkConfig.client_id}&client_secret={SdkConfig.client_secret}"
    result = requests.post(url, json=data.dict(exclude_none=True, by_alias=True))
    return result.json()
