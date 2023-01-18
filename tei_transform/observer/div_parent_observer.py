from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DivParentObserver(AbstractNodeObserver):
    """
    Observer for <div/> elements with invalid parent.
    """

    def observe(self, node: etree._Element) -> bool:
        valid_div_parents = {"div", "body", "lem", "rdg", "back", "front"}
        if etree.QName(node).localname == "div":
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname not in valid_div_parents
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
