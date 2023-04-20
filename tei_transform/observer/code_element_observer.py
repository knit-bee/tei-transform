from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    remove_attribute_from_node,
)


class CodeElementObserver(AbstractNodeObserver):
    """
    Observer for <code/> elements that have descendants.

    Find <code/> elements that have other elements as descendants
    and change their tag to <ab/> and set @type='code' attribute.
    If the <code/> element has @lang attribute, the attribute is
    removed and the value concatenated with the type attribute
    (if it was newly added).
    If the parent of <code/> has tag </p> or <ab/>, the <code/>
    element is added as next sibling of its parent.
    If the <code/> element has following siblings, a new element
    with the same tag as the parent is added as next to
    the former <code/> element and the sibling elements are
    added to this new element.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "code" and len(node) != 0:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "ab")
        if node.attrib.get("type", None) is None:
            type_attr_value = "code"
            if (lang_value := node.attrib.get("lang", None)) is not None:
                type_attr_value = f"{type_attr_value}-{lang_value}"
            node.set("type", type_attr_value)
        remove_attribute_from_node(node, "lang")
