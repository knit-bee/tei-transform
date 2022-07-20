from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class SchemaLocationObserver(AbstractNodeObserver):
    xpattern = ""

    def observe(self, node: etree._Element) -> bool:
        ns_mapping = node.nsmap
        if (
            node.tag == etree.QName(ns_mapping[None], "TEI").text
            and etree.QName(ns_mapping.get("xsi", None), "schemaLocation")
            in node.attrib
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
