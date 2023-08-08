import re

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivTextObserver(AbstractNodeObserver):
    """
    Observer for text in <div> elements


    Find <div/> elements that contain text and add the text to a new
    child element <p/>. If the text consists only of one character, it
    is added to the first <p/> child element.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "div" and node.text is not None:
            if node.text.strip("\n \t"):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if node.text.strip():
            self._handle_real_text_tail(node)
        else:
            self._substitute_whitespace_chars(node)

    def _handle_real_text_tail(self, node: etree._Element) -> None:
        if len(node.text) == 1:
            if node.getchildren() and etree.QName(node[0]).localname == "p":
                first_child = node[0]
                first_child.text = node.text + first_child.text
                node.text = None
                return

        new_child = create_new_element(node, "p")
        new_child.text = node.text
        node.text = None
        node.insert(0, new_child)

    def _substitute_whitespace_chars(self, node: etree._Element) -> None:
        node.text = re.sub(r"\s", " ", node.text)
