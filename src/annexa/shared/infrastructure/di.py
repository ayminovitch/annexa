from annexa.shared.domain.time import Clock, SystemClock


class Container:
    def __init__(self) -> None:
        self.clock: Clock = SystemClock()


_container = Container()


def get_container() -> Container:
    return _container
