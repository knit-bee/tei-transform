from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class ListAsDivSiblingObserver(AbstractNodeObserver):
    """
    Observer for <list/> elements that are following siblings of <div/>.

    Find <list/> elements that are siblings of <div/> and add a new
    <div/> as parent of <list/>.

    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if list(node.itersiblings("{*}div", preceding=True)) != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        sibling = node.getprevious()
        new_element = create_new_element(node, "div")
        if sibling is not None:
            sibling.addnext(new_element)
        else:
            parent = node.getparent()
            parent.insert(0, new_element)
        new_element.append(node)
