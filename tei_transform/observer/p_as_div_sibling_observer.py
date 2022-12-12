from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class PAsDivSiblingObserver(AbstractNodeObserver):
    """
    Observer for <p/> elements that are siblings of <div/>.

    Find <p/> elements that are direct siblings of <div/> elements
    and insert a new <div/> as parent of <p/>. Multiple <p/> after the
    same <div/> will be united under the same new <div/> element.
    """

    _new_element: Optional[list] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            if (
                node.getparent() is not None
                and list(node.getparent().iterchildren("{*}div")) != []
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if (node.text is not None and node.text.strip()) or (
            node.tail is not None and node.tail.strip()
        ):
            sibling = node.getprevious()
            if sibling is not None:
                if self._new_element is sibling:
                    self._new_element.append(node)
                else:
                    new_element = create_new_element(node, "div")
                    sibling.addnext(new_element)
                    self._new_element = new_element
                    new_element.append(node)
            else:
                parent = node.getparent()
                new_element = create_new_element(node, "div")
                parent.insert(0, new_element)
                new_element.append(node)
                self._new_element = new_element
        else:
            node.getparent().remove(node)
