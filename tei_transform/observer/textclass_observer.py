from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class TextclassObserver(AbstractNodeObserver):
    """Observer for  <textclass> elements.
    Find <textclass> element and replace tag with 'textClass'
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "textclass":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "textClass")
