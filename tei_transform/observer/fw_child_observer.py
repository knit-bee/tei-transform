from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag, merge_into_parent


class FwChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <list/> elements with <fw/> parent.

    Find <p/> and <list/> elements that are children of <fw/>.

    If the target element has tag 'p', it is merge into the
    parent by stripping the inner element (text, tail, and
    children are not removed).

    If the target element has tag 'list', the tag of the
    parent is changed to 'ab'.
    N.B.:
    - Use in combination with DoublePlikeObserver to
    avoid invalid structure if the <fw/> parent contains
    <p/> and <list/>.
    - Use in combination with NestedFwWithListObserver to avoid
    nesting of <fw/> and <ab/>.
    """

    def observe(self, node: etree._Element) -> bool:
        target_tags = {"p", "list"}
        if etree.QName(node).localname in target_tags:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "fw":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if etree.QName(node).localname == "p":
            merge_into_parent(node)
        if etree.QName(node).localname == "list":
            change_element_tag(node.getparent(), "ab")
