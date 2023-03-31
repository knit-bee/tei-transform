from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class UlElementObserver(AbstractNodeObserver):
    """
    Observer for <ul/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "ul":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
