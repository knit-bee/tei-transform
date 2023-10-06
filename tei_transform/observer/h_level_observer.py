from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class HLevelObserver(AbstractNodeObserver):
    """
    Observer for <h#/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if len(tag := etree.QName(node).localname) == 2:
            if tag.startswith("h") and tag[1].isnumeric():
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
