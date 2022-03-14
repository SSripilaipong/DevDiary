from lib.chamber.transaction import OptimisticLockFailed


class EntityOutdated(OptimisticLockFailed):
    pass
