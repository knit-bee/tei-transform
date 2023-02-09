from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_text_content


class NestedFwWithListObserver(AbstractNodeObserver):
    """
    Observer for <fw/> with <fw/> parent and a <list/> descendant.

    Find <fw/> elements with <fw/> parent and that have a
    <list/> element as descendant, which in turn is a child
    of <fw/> or <p/>.The target <fw/> is added as sibling of
    the parent and any following siblings are transferred to
    a new <fw/> element that is added as following sibling of
    the target element.
    Any type or rendition attributes of the parent are also
    added to the new <fw/> element.
    If the target element has tail, the tail is added to the
    tail of the last child.
    If the parent is empty after the transformation, it will be
    removed.
    N.B.: Multiple nested <fw/> elements are not per se invalid
    according to TEI P5, however this transformation should be
    used in combination with FwChildObserver to avoid nesting
    of <fw/> and <ab/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "fw":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "fw":
                list_descendant = node.find(".//{*}list")
                if list_descendant is not None and etree.QName(
                    list_descendant.getparent()
                ).localname in {"fw", "p"}:
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        grandparent = parent.getparent()
        following_siblings = list(node.itersiblings())
        if following_siblings:
            new_fw = create_new_element(node, "fw")
            new_fw.extend(following_siblings)
            for attr, val in parent.attrib.items():
                if attr in {
                    "rend",
                    "style",
                    "rendition",
                    "type",
                }:
                    new_fw.set(attr, val)
            grandparent.insert(grandparent.index(parent) + 1, new_fw)
        grandparent.insert(grandparent.index(parent) + 1, node)
        if node.tail is not None and node.tail.strip():
            node[-1].tail = merge_text_content(node[-1].tail, node.tail)
            node.tail = None
        if (
            len(parent) == 0
            and (parent.text is None or not parent.text.strip())
            and (parent.tail is None or not parent.tail.strip())
        ):
            grandparent.remove(parent)
