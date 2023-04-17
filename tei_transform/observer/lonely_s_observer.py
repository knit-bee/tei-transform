from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class LonelySObserver(AbstractNodeObserver):
    """
    Observer for <s/> elements with <body/> or <div/> as parent
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "s":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in {"div", "body"}:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
