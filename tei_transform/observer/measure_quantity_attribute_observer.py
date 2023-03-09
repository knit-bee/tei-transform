from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class MeasureQuantityAttributeObserver(AbstractNodeObserver):
    """
    Observer for <term/> elements with @measure_quantity attribute.

    Find <term/> elements with attribute @measure_quantity and remove
    attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "term" and "measure_quantity" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "measure_quantity")
