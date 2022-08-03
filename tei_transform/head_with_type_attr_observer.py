from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class HeadWithTypeAttrObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        qname = etree.QName(node.tag)
        if qname.localname == "head" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
