"""
Iterate over xml-Tree while observers scan incoming nodes for their
respective pattern. If an observer finds a match, the corresponding
action is performed on the node.
"""
from typing import List

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class XMLTreeIterator:
    def __init__(self, list_of_observers: List[AbstractNodeObserver]):
        self.observers = list_of_observers

    def iterate_xml(self, file: str) -> etree._Element:
        root = []
        for event, node in etree.iterparse(
            file, events=["start", "end"], tag=["{*}TEI", "{*}teiHeader", "{*}text"]
        ):
            qname = etree.QName(node.tag)
            if event == "start":
                if qname.localname == "TEI":
                    root = self.construct_new_tei_root(node)
                continue
            else:
                if qname.localname == "TEI":
                    continue
                # do node cleaning here
                root.append(node)
        return root

    def construct_new_tei_root(self, old_node: etree._Element) -> etree._Element:
        ns_prefix = old_node.nsmap.get(None, None)
        if ns_prefix is not None:
            qname = etree.QName(ns_prefix, "TEI")
        else:
            qname = "TEI"
        return etree.Element(qname, attrib=old_node.attrib, nsmap=old_node.nsmap)
