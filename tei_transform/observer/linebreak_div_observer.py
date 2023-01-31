from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class LinebreakDivObserver(AbstractNodeObserver):
    """
    Observer for <lb/> elements with tail and <div/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "lb"
            and etree.QName(node.getparent()).localname == "div"
        ):
            if node.tail is not None and node.tail.strip():
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
