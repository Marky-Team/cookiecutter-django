import datetime
from enum import Enum
from functools import wraps
from typing import Any
from uuid import UUID


def inject_test_counter(func):
    func.counter = 0

    @wraps(func)
    def wrap(*args, **kwargs):
        func.counter += 1
        return func(func.counter, *args, **kwargs)

    return wrap


class TestSentinels(Enum):
    NOT_SET = "NOT_SET"


def datetime_to_drf_string(dt: datetime.datetime) -> str:
    """Should return in the format '2024-06-23T03:38:14.691415Z'"""
    return dt.astimezone(datetime.UTC).isoformat()[:26] + "Z"


def datetime_2000_plus_sec(seconds_to_add: int) -> datetime.datetime:
    dt = datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC)
    dt += datetime.timedelta(seconds=seconds_to_add)
    return dt


def neg_1_if_odd_else_1(value: int) -> int:
    if value % 2 == 1:
        return -1
    return 1


def as_drf(input_value: Any) -> Any:
    """
    Handles the weird intricacies that DRF does when rendering Python data types to
    output JSON. This is only to be used in tests as a convenience method to not have
    to coerce your Python datatypes to show DRF renders them;
    THIS SHOULD NOT BE USED TO RENDER API RESPONSES TO USERS.
    :param input_value: Any python value is allowed
    :return: How DRF would generally represent this in JSON with default settings.
    """
    if isinstance(input_value, datetime.datetime):
        value = input_value.isoformat()
        if value.endswith("+00:00"):
            value = value[:-6] + "Z"
        return value

    if isinstance(input_value, UUID):
        return str(input_value)

    if isinstance(input_value, Enum):
        return input_value.value

    if isinstance(input_value, dict):
        for k, v in input_value.items():
            input_value[k] = as_drf(v)
        return input_value

    return input_value
