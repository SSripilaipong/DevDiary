from typing import Union


def _validate_min_value_config(min_value) -> Union[int, float]:
    if min_value is not None:
        if not isinstance(min_value, int):
            raise TypeError(f"MIN_VALUE config should be integer (got {min_value}).")
        return min_value
    return 0


def _validate_max_value_config(max_length) -> Union[int, float]:
    if max_length is not None:
        assert isinstance(max_length, int)
        return max_length
    return float('inf')
