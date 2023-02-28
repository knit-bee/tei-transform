from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class BodyWithTextObserver(AbstractNodeObserver):
    """
    Observer for <body/> elements that contain text.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "body"
            and node.text is not None
            and node.text.strip()
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_p = create_new_element(node, "p")
        new_p.text = node.text
        node.text = None
        node.insert(0, new_p)
