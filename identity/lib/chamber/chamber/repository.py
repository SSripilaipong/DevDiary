from chamber.transaction import OptimisticLockFailed


class EntityOutdated(OptimisticLockFailed):
    pass
