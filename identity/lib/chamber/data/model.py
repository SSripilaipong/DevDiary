from typing import Dict, Set


class DataModel:
    def __init__(self, **kwargs):
        self.__chamber_assign_fields(kwargs)

    def __chamber_assign_fields(self, data: Dict):
        provided_keys = set(data)
        required_keys = self.__chamber_get_keys_from_annotations()
        _validate_initial_values(provided_keys, required_keys)

    def __chamber_get_keys_from_annotations(self) -> Set[str]:
        from chamber.aggregate import Field

        return set(name for name in getattr(self, '__annotations__', {}).keys()
                   if isinstance(vars(self.__class__).get(name, None), Field))


def _validate_initial_values(provided_keys, required_keys):
    exceeded_keys = provided_keys - required_keys
    lacked_keys = required_keys - provided_keys

    if exceeded_keys != set():
        message = "Unknown fields named: " + ', '.join(list(exceeded_keys))
        raise AttributeError(message)
