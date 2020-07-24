# -*- coding: utf-8 -*-
from datetime import datetime
import re
import json
from uuid import UUID
import hmac
import base64


def try_int(_str):
    """
    преобразование в целое число с обработкой исключения
    :return:
    """

    try:
        return int(_str)
    except Exception:
        return None


def try_float(_str):
    """
    преобразование в действительное число с обработкой исключения
    :return:
    """

    try:
        return float(_str)
    except Exception:
        return None


def is_none_or_space(_string):

    if _string is None or not isinstance(_string, str) or len(_string.strip()) == 0:
        return True
    else:
        return False


def is_empty_iterable(iter_):

    if not isinstance(iter_, list) and not isinstance(iter_, set):
        return True
    elif len(iter_) == 0:
        return True
    else:
        return False


def none_raise_exception(checked):

    if isinstance(checked, list):
        for val in checked:
            if val is None:
                raise Exception('None exception')

        return True

    else:
        if checked is None:
            raise Exception('None exception')
        return True


def get_unique_dict_list(l: list) -> list:
    return list({str(v): v for v in l}.values())


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def sign_hs256(msg: str, secret: str) -> str:
    hm = hmac.new(secret.encode('utf-8'), msg=msg.encode('utf-8'), digestmod='sha256')
    binary_signature = hm.digest()
    signature = base64.b64encode(binary_signature).decode('utf-8')
    return re.sub(r'=+$', '', signature)


def verify_hs256(msg: str, secret: str, sign: str) -> bool:
    calculated_sign = sign_hs256(msg, secret)
    return hmac.compare_digest(calculated_sign, sign)