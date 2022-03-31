from chamber.usecase.usecase import T, Usecase


def usecase(func: T) -> T:
    return Usecase(func)