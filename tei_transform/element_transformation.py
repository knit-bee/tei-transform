from typing import Optional

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
        node.tag = etree.QName(ns_prefix, new_name)


def construct_new_tei_root(old_node: etree._Element) -> etree._Element:
    ns_prefix = old_node.nsmap.get(None, None)
    qname = etree.QName(ns_prefix, "TEI").text
    return etree.Element(qname, attrib=old_node.attrib, nsmap=old_node.nsmap)
