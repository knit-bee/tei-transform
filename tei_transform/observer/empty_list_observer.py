from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class EmptyListObserver(AbstractNodeObserver):
    """
    Observer for empty <list/> elements.

    Find <list/> elements that don't contain any <item/> elements
    or text and remove them.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if not len(node) and (node.text is None or not node.text.strip()):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if node.tail and node.tail.strip():
            tail_text = node.tail
            new_p = create_new_element(node, "p")
            new_p.text = tail_text
            parent_tag = etree.QName(parent).localname
            if parent_tag in {"p", "item", "cell", "ab", "fw", "quote", "head"}:
                if parent.text:
                    parent.text += " " + tail_text
                else:
                    parent.text = tail_text
            else:
                node.addnext(new_p)
        parent.remove(node)
