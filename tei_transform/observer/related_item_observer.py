from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class RelatedItemObserver(AbstractNodeObserver):
    """
    Observer for <relatedItem/> elements without children.

    Find <relatedItem/> elements that do not have any children
    (but possibly contain text) and remove them. If the <relatedItem/>
    element has the attribute '@target', it will not be removed.
    If the parent element of <relatedItem/> would be empty after removal,
    it will also be removed.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "relatedItem" and len(node) == 0:
            if "target" not in node.attrib:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        parent.remove(node)
        if len(parent) == 0:
            grandparent = parent.getparent()
            grandparent.remove(parent)
