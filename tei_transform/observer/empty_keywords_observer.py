from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class EmptyKeywordsObserver(AbstractNodeObserver):
    """
    Observer for empty <keywords/> elements.

    Find empty <keywords/> elements and add an empty <term/>
    as child.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "keywords" and len(node) == 0:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        term_child = create_new_element(node, "term")
        node.append(term_child)
