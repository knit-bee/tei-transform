from typing import Dict, Optional, Union

from lxml import etree


def remove_attribute_from_node(
    node: etree._Element, attribute: str, namespace: Optional[str] = None
) -> None:
    """
    Remove an attribute from a node.
    """
    if namespace:
        xml_ns = node.nsmap[namespace]
        attribute = etree.QName(xml_ns, attribute)
    node.attrib.pop(attribute, None)


def add_namespace_prefix_to_attribute(
    node: etree._Element, old_attr: str, namespace: str
) -> None:
    """
    Add a namespace prefix to an attribute.
    The namespace argument should contain the URI reference of the
    namespace, e.g. for 'xml'
    namespace="http://www.w3.org/XML/1998/namespace"
    """
    old_attribute = node.attrib.get(old_attr)
    if old_attribute is not None:
        attr_value = node.attrib.pop(old_attr)
        new_attribute = etree.QName(namespace, old_attr)
        node.set(new_attribute, attr_value)


def change_element_tag(node: etree._Element, new_name: str):
    """
    Change the tag of a node.
    All other properties of the node (like children and attributes)
    won't be affected.
    """
    ns_prefix = node.nsmap.get(None, None)
    if ns_prefix is None:
        node.tag = new_name
    else:
        node.tag = etree.QName(ns_prefix, new_name).text


def construct_new_tei_root(
    old_node: etree._Element, ns_to_add: Optional[Dict[Union[str, None], str]] = None
) -> etree._Element:
    new_namespace = old_node.nsmap
    if ns_to_add is not None:
        new_namespace.update(ns_to_add)
    ns_prefix = new_namespace.get(None, None)
    qname = etree.QName(ns_prefix, "TEI").text
    return etree.Element(qname, attrib=old_node.attrib, nsmap=new_namespace)


def create_new_element(old_node: etree._Element, new_tag: str) -> etree._Element:
    ns_prefix = old_node.nsmap.get(None, None)
    new_element_tag = etree.QName(ns_prefix, new_tag).text
    new_element = etree.Element(new_element_tag)
    return new_element


def merge_text_content(
    first_part: Optional[str], second_part: Optional[str]
) -> Optional[str]:
    if second_part is None or not second_part.strip():
        return first_part
    if first_part is None or not first_part.strip():
        return second_part.strip() if second_part is not None else second_part
    return " ".join([first_part.strip(), second_part.strip()])
