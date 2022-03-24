from typing import Union


def _validate_min_value_config(min_value) -> Union[int, float]:
    if min_value is not None:
        if not isinstance(min_value, int):
            raise TypeError(f"MIN_VALUE config should be integer (got {min_value}).")
        return min_value
    return 0


def _validate_max_value_config(max_value) -> Union[int, float]:
    if max_value is not None:
        if not isinstance(max_value, int):
            raise TypeError(f"MAX_VALUE config should be integer (got {max_value}).")
        assert isinstance(max_value, int)
        return max_value
    return float('inf')
