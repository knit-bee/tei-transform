from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class HeadAfterPElementObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        qname = etree.QName(node.tag)
        if qname.localname == "head":
            older_sibling = node.getprevious()
            if (
                older_sibling is not None
                and etree.QName(older_sibling.tag).localname == "p"
            ):
                return True
            return False
        return False

    def transform_node(self, node: etree._Element) -> None:
        if node.text:
            change_element_tag(node, "ab")
            node.set("type", "head")
        else:
            node.getparent().remove(node)
