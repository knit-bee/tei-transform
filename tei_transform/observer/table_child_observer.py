from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class TableChildObserver(AbstractNodeObserver):
    """
    Observer for invalid children of <table/>.

    Find <p/> elements that are children of <table/> and change
    their tag to <fw/>. If the element is empty, it is removed
    instead.

    To handle tails on invalid children, use in combination with
    TableTextObserver.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "table":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            node.getparent().remove(node)
        else:
            change_element_tag(node, "fw")
