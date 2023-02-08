from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DoubleFwObserver(AbstractNodeObserver):
    """
    Observer for <fw/> elements with child and <fw/> parent.

    Find <fw/> elements with <fw/> parent and have themselves
    children with tag 'fw' or 'list'. The target <fw/> is added
    as sibling of the parent and any following siblings are
    transferred to a new <fw/> element that is added as following
    sibling of the target element.
    Any type or rendition attributes of the parent are also
    added to the new <fw/> element.
    If the parent is empty after the transformation, it will be
    removed.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "fw":
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname == "fw"
                and list(node.iterchildren(["{*}list", "{*}fw"])) != []
            ):
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
        if (
            len(parent) == 0
            and (parent.text is None or not parent.text.strip())
            and (parent.tail is None or not parent.tail.strip())
        ):
            grandparent.remove(parent)
