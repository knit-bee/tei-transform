"""
Iterate over xml-file and yield nodes relevant for TEI valid xml.
"""
from typing import Generator

from lxml import etree


class XMLTreeIterator:
    def iterate_xml(self, file: str) -> Generator[etree._Element, None, None]:
        for event, node in etree.iterparse(
            file, events=["start", "end"], tag=["{*}TEI", "{*}teiHeader", "{*}text"]
        ):
            qname = etree.QName(node.tag)
            if event == "start":
                if qname.localname == "TEI":
                    root = self.construct_new_tei_root(node)
                    yield root
                continue
            else:
                if qname.localname == "TEI":
                    continue
                yield node

    def construct_new_tei_root(self, old_node: etree._Element) -> etree._Element:
        ns_prefix = old_node.nsmap.get(None, None)
        if ns_prefix is not None:
            qname = etree.QName(ns_prefix, "TEI")
        else:
            qname = "TEI"
        return etree.Element(qname, attrib=old_node.attrib, nsmap=old_node.nsmap)
