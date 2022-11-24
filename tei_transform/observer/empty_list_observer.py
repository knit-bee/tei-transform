from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class EmptyListObserver(AbstractNodeObserver):
    """
    Observer for empty <list/> elements.

    Find <list/> elements that don't contain any <item/>
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if not len(node):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
