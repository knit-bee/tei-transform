from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class CliRequest:
    file: str
    observers: List[str]


class TeiTransformationUseCase(Protocol):
    def process(self, request: CliRequest) -> None:
        ...


class TeiTransformationUseCaseImpl:
    def process(self, request: CliRequest) -> None:
        pass
