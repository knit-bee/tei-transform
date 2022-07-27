from dataclasses import dataclass
from typing import List, Optional, Protocol

from lxml import etree

from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.revision_desc_change import construct_change_from_config_file
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator


@dataclass
class CliRequest:
    file: str
    observers: List[str]
    config: Optional[str] = None


class TeiTransformationUseCase(Protocol):
    def process(self, request: CliRequest) -> None:
        ...


class TeiTransformationUseCaseImpl:
    """
    Use case that is called by console script.
    """

    def process(self, request: CliRequest) -> etree._Element:
        """
        Processes cli arguments and applies them for the transformation
        of an xml tree. The transformed tree is returned.
        """
        tree_iterator = XMLTreeIterator()
        constructor = ObserverConstructor()
        observer_list = constructor.construct_observers(request.observers)
        transformer = TeiTransformer(
            xml_iterator=tree_iterator, list_of_observers=observer_list
        )
        new_tree = transformer.perform_transformation(request.file)
        if request.config is not None:
            change = construct_change_from_config_file(request.config)
            if transformer.xml_tree_changed() and change is not None:
                transformer.add_change_to_revision_desc(new_tree, change)
        return new_tree
