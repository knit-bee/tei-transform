from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


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
        if node.text is not None and node.text.strip():
            sibling = node.getprevious()
            if self._new_element is sibling:
                self._new_element.append(node)
            else:
                ns_prefix = node.nsmap.get(None, None)
                new_element_tag = etree.QName(ns_prefix, "div")
                new_element = etree.Element(new_element_tag)
                sibling.addnext(new_element)
                self._new_element = new_element
                new_element.append(node)
        else:
            node.getparent().remove(node)
