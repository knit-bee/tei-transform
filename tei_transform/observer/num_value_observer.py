from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class NumValueObserver(AbstractNodeObserver):
    """
    Observer for <num/> elements with @value='percent' attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "num":
            value_attrib = node.attrib.get("value", None)
            if value_attrib == "percent":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
