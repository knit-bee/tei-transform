from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class DoubleItemObserver(AbstractNodeObserver):
    """
    Observer for <item/> elements that are children of <item/>

    Find <item/> elements that are children of <item/>. If the
    inner <item/> element has children of its own, a new parent
    <list/> will be inserted to wrap the inner <item/>, else
    the tag of the inner <item/> will be changed to <ab/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "item":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "item":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if not node.getchildren():
            change_element_tag(node, "ab")
        else:
            parent = node.getparent()
            ns_prefix = node.nsmap.get(None, None)
            new_node_tag = etree.QName(ns_prefix, "list").text
            new_list_node = etree.Element(new_node_tag)
            node_index = parent.index(node)
            parent.insert(node_index, new_list_node)
            new_list_node.append(node)
