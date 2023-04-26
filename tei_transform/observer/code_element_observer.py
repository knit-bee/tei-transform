from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    create_new_element,
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
        self._handle_attributes(node)
        parent = node.getparent()
        parent_tag = etree.QName(parent).localname
        if parent_tag in {"p", "ab"}:
            self._resolve_hierarchy_with_p_like_parent(node, parent, parent_tag)

    def _handle_attributes(self, element: etree._Element) -> None:
        if element.attrib.get("type", None) is None:
            type_attr_value = "code"
            if (lang_value := element.attrib.get("lang", None)) is not None:
                type_attr_value = f"{type_attr_value}-{lang_value}"
            element.set("type", type_attr_value)
        remove_attribute_from_node(element, "lang")

    def _resolve_hierarchy_with_p_like_parent(
        self, element: etree._Element, parent: etree._Element, parent_tag: str
    ) -> None:
        grand_parent = parent.getparent()
        parent_index = grand_parent.index(parent)
        following_siblings = list(element.itersiblings())
        if following_siblings:
            new_parent = create_new_element(element, parent_tag)
            grand_parent.insert(parent_index + 1, new_parent)
            new_parent.extend(following_siblings)
        grand_parent.insert(parent_index + 1, element)
