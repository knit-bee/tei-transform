from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class BylineSiblingObserver(AbstractNodeObserver):
    """
    Observer for <byline/> elements that are followed by a <p/> or <div/>.

    Find <byline/> elements that have a <p/> or a <div/> element as next
    sibling and add a new <div/> element wrapping the <byline/> and any
    siblings before (up to <div/> if present). The following <p/> sibling
    is not touched, i.e. it will now appear as a sibling of <div/>. To
    avoid this invalid structure, use togehter with PAsDivSiblingObserver .
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "byline":
            sibling = node.getnext()
            if sibling is not None and etree.QName(sibling).localname == "p":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        older_siblings = []
        for sibling in node.itersiblings(preceding=True):
            if etree.QName(sibling).localname == "div":
                break
            older_siblings.append(sibling)
        new_div = create_new_element(node, "div")
        node_index = parent.index(node)
        parent.insert(node_index, new_div)
        for sibling in reversed(older_siblings):
            new_div.append(sibling)
        new_div.append(node)
