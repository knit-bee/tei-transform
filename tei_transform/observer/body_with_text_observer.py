from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_text_content


class BodyWithTextObserver(AbstractNodeObserver):
    """
    Observer for <body/> elements that contain text.

    Find <body/> elements that contain text and add text content
    to the first child if it can contain text. Else, add text
    to a new <p/> element that is inserted as first child of
    <body/>.
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
        if len(node) == 0 or etree.QName(node[0]).localname in {
            "div",
            "list",
            "table",
        }:
            new_p = create_new_element(node, "p")
            new_p.text = node.text
            node.insert(0, new_p)
        else:
            first_child = node[0]
            first_child.text = merge_text_content(node.text, first_child.text)
        node.text = None
