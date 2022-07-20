from dataclasses import dataclass
from typing import List, Protocol

from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator


@dataclass
class CliRequest:
    file: str
    observers: List[str]


class TeiTransformationUseCase(Protocol):
    def process(self, request: CliRequest) -> None:
        ...


class TeiTransformationUseCaseImpl:
    def process(self, request: CliRequest) -> None:
        tree_iterator = XMLTreeIterator()
        constructor = ObserverConstructor()
        observer_list = constructor.construct_observers(request.observers)
        transformer = TeiTransformer(
            xml_iterator=tree_iterator, list_of_observers=observer_list
        )
        return transformer.perform_transformation(request.file)
