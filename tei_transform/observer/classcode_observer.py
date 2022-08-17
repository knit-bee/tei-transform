from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class ClasscodeObserver(AbstractNodeObserver):
    """Observer for  <classcode/> elements.

    Find <classcode/> element and replace tag with 'classCode'
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "classcode":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "classCode")
