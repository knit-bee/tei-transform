from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    remove_attribute_from_node,
)


class HLevelObserver(AbstractNodeObserver):
    """
    Observer for <h#/> elements.

    Change tag of elements with 'h#' tag (e.g. 'h2') to 'ab' and add
    @type='head' and @rend with the old tag name as value.
    Invalid attributes, such as @class and @title, are removed.
    """

    def observe(self, node: etree._Element) -> bool:
        if len(tag := etree.QName(node).localname) == 2:
            if tag.startswith("h") and tag[1].isnumeric():
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        old_tag = etree.QName(node).localname
        change_element_tag(node, "ab")
        node.set("type", "head")
        node.set("rend", old_tag)
        unwanted_attributes = ["class", "title"]
        for attr in unwanted_attributes:
            remove_attribute_from_node(node, attr)
