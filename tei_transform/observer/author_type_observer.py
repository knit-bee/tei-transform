from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class AuthorTypeObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "author" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
