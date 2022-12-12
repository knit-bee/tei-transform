from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class SchemaLocationObserver(AbstractNodeObserver):
    """
    Observer for 'schemaLocation' attribute on <TEI/> elements

    Find 'schemaLocation' attribute in <TEI/> nodes and removed it.
    """

    def observe(self, node: etree._Element) -> bool:
        ns_mapping = node.nsmap
        if (
            etree.QName(node).localname == "TEI"
            and etree.QName(ns_mapping.get("xsi", None), "schemaLocation")
            in node.attrib
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        attrib_ns = None
        if node.nsmap:
            attrib_ns = "xsi"
        remove_attribute_from_node(node, "schemaLocation", attrib_ns)
