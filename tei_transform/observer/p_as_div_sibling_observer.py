from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class PAsDivSiblingObserver(AbstractNodeObserver):
    """
    Observer for <p/> elements that are following siblings of <div/>.

    Find <p/> elements that are direct siblings of <div/> elements
    and insert a new <div/> as parent of <p/>. Multiple <p/> after the
    same <div/> will be united under the same new <div/> element. If the
    <p/> element is empty, it is removed.
    """

    def __init__(self) -> None:
        self._new_element: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            if list(node.itersiblings("{*}div", preceding=True)) != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if (
            len(node) != 0
            or (node.text is not None and node.text.strip())
            or (node.tail is not None and node.tail.strip())
        ):
            self._reset_last_created_new_div_if_necessary()
            sibling = node.getprevious()
            if sibling is None or sibling != self._new_element:
                new_element = create_new_element(node, "div")
                parent = node.getparent()
                parent.insert(parent.index(node), new_element)
                self._new_element = new_element
            self._new_element.append(node)
        else:
            node.getparent().remove(node)

    def _reset_last_created_new_div_if_necessary(self) -> None:
        if self._new_element is not None:
            if list(self._new_element.iterchildren("{*}div")) != []:
                self._new_element = None
