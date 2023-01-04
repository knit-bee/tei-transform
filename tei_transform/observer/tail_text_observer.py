from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class TailTextObserver(AbstractNodeObserver):
    """
    Observer for elements with text in tail.

    Search for elements with tags <p>, <fw> or <ab> that
    are descendants of <div>, <body>, or <floatingText> and
    contain text in their tail. The text in the element tail
    will be removed and added to a new sibling element with
    tag <p>. If the element has tag <fw> and is a direct descendant
    of <floatingText>, the tag <fw> will be used instead of <p>.
    """

    def observe(self, node: etree._Element) -> bool:
        node_local_tag = etree.QName(node).localname
        if node_local_tag in {"p", "ab", "fw"}:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in {
                "div",
                "body",
                "floatingText",
            }:
                if node.tail is not None and node.tail.strip():
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        tail_text = node.tail
        if (
            etree.QName(node).localname == "fw"
            and etree.QName(node.getparent()).localname == "floatingText"
        ):
            new_elem = create_new_element(node, "fw")
        else:
            new_elem = create_new_element(node, "p")
        new_elem.text = tail_text
        node.tail = None
        node.addnext(new_elem)
