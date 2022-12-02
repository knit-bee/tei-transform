from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class RelatedItemObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "relatedItem" and len(node) == 0:
            if "target" not in node.attrib:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
