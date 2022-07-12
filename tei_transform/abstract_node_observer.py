from abc import ABC, abstractmethod

from lxml import etree


class AbstractNodeObserver(ABC):
    @abstractmethod
    def observe(self, node: etree._Element) -> bool:
        """
        This method should implement the rules according to which a node is
        recognized by the observer.
        """
        pass
