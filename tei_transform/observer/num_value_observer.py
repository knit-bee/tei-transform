from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class NumValueObserver(AbstractNodeObserver):
    """
    Observer for <num/> elements with @value='percent' attribute.

    Change name of @value attribute to @type if value is 'percent'.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "num":
            value_attrib = node.attrib.get("value", None)
            if value_attrib == "percent":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        value_attrib = node.attrib.pop("value")
        node.set("type", value_attrib)
