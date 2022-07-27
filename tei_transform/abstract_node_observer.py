from abc import ABC, abstractmethod

from lxml import etree


class AbstractNodeObserver(ABC):
    """Abstract class for implementation of observers applied by TeiTransformer"""

    @abstractmethod
    def observe(self, node: etree._Element) -> bool:
        """
        This method should implement the rules according to which a node is
        recognized by the observer.
        """
        pass

    @abstractmethod
    def transform_node(self, node: etree._Element) -> None:
        """
        This method should implement the action to perform on nodes that
        the observer activates on."""
        pass
