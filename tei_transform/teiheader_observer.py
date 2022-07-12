from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class TeiHeaderObserver(AbstractNodeObserver):
    """Find 'type' attribute in <teiHeader> element"""

    xpattern = "//teiHeader[@type]"

    def observe(self, node: etree._Element) -> bool:
        if node.tag == "teiHeader" and "type" in node.attrib:
            return True
        return False
