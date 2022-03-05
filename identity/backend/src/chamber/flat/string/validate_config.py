from typing import Set, List, Union


def _validate_min_length_config(min_length) -> int:
    if min_length is not None:
        assert isinstance(min_length, int)
        return min_length
    return 0


def _validate_max_length_config(max_length) -> Union[int, float]:
    if max_length is not None:
        assert isinstance(max_length, int)
        return max_length
    return float('inf')


def _validate_valid_characters_config(valid_characters) -> Set[str]:
    if valid_characters is not None:
        assert isinstance(valid_characters, (str, set, list, tuple))
        return set(valid_characters)
    return set()


def _validate_required_character_config(required_characters) -> List[Set[str]]:
    if required_characters is not None:
        if isinstance(required_characters, str):
            return [set(required_characters)]
        assert isinstance(required_characters, (list, tuple))
        return [set(_set) for _set in required_characters]
    return []
