from typing import Union


def _validate_min_value_config(min_length) -> Union[int, float]:
    if min_length is not None:
        assert isinstance(min_length, int)
        return min_length
    return 0


def _validate_max_value_config(max_length) -> Union[int, float]:
    if max_length is not None:
        assert isinstance(max_length, int)
        return max_length
    return float('inf')
