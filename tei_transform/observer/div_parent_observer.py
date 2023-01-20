from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class DivParentObserver(AbstractNodeObserver):
    """
    Observer for <div/> elements with invalid parent.

    Find <div/> elements that are not descendants of <body/>, <back/>,
    <front/> or other <div/> elements or <lem/> or <rdg/>.
    If the tag of the parent element is <p/> or <ab/>, the parent tag
    will be changed to <div/>, for all other tags the invalid <div/>
    element will be stripped from the tree by merging its children, text
    and tail into the parent element.
    N.B. If the parent element has <p/> or <ab/>, this transformation
    might result in an invalid tree, e.g.:
        - if the parent contains text or children with tail or tags that
            are no valid descendants of <div/>
        - if the parent has e.g. other <p/> as siblings
    """

    def observe(self, node: etree._Element) -> bool:
        valid_div_parents = {"div", "body", "lem", "rdg", "back", "front"}
        if etree.QName(node).localname == "div":
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname not in valid_div_parents
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        p_like_tags = {"p", "ab"}
        parent = node.getparent()
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            parent.remove(node)
            return
        if etree.QName(parent).localname in p_like_tags:
            change_element_tag(parent, "div")
            return
        node.tag = "tempRename"
        etree.strip_tags(parent, "tempRename")
