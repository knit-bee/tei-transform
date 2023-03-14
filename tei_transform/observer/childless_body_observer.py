from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class ChildlessBodyObserver(AbstractNodeObserver):
    """
    Observer for <body/> elements without children.

    Find <body/> elements that don't have any children and add
    an empty <p/> element. If the <body/> element contains text,
    it will be removed and added as text content of the new <p/>.
    """

    def observe(self, node: etree._Element) -> bool:
        required_children = {"p", "ab", "quote", "list", "table", "div"}
        if (
            etree.QName(node).localname == "body"
            and [
                child
                for child in node.iterchildren()
                if etree.QName(child).localname in required_children
            ]
            == []
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_p = create_new_element(node, "p")
        if node.text is not None and node.text.strip():
            new_p.text = node.text
            node.text = None
        node.append(new_p)
