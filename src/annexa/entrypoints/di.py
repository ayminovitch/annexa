from annexa.shared.domain.time import Clock, SystemClock
from annexa.regulation.application.ports import LLMProvider
from annexa.regulation.infrastructure.llm_google import GoogleGenAIProvider


class Container:
    def __init__(self) -> None:
        self.clock: Clock = SystemClock()
        self.llm_provider: LLMProvider = GoogleGenAIProvider()

_container = Container()

def get_container() -> Container:
    return _container
