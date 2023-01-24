from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class LonelyItemObserver(AbstractNodeObserver):
    """
    Observer for <item/> elements outside <list/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "item" and etree.QName(
            node.getparent()
        ).localname not in {"item", "list"}:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
