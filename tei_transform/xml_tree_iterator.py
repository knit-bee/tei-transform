"""
Iterate over xml-file and yield nodes relevant for TEI valid xml.
"""
from typing import Generator

from lxml import etree

from tei_transform.element_transformation import construct_new_tei_root


class XMLTreeIterator:
    def iterate_xml(self, file: str) -> Generator[etree._Element, None, None]:
        """
        Iterate over xml file and yield the nodes <TEI>, <teiHeader>
        and <text>.
        """
        for event, node in etree.iterparse(
            file, events=["start", "end"], tag=["{*}TEI", "{*}teiHeader", "{*}text"]
        ):
            qname = etree.QName(node.tag)
            if event == "start":
                if qname.localname == "TEI":
                    root = construct_new_tei_root(node)
                    yield root
                continue
            else:
                if qname.localname == "TEI":
                    continue
                yield node
