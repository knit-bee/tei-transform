from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class NoteStmtObserver(AbstractNodeObserver):
    """Find 'type' attribute in <noteStmt> elements"""

    xpattern = "//noteStmt[@type]"

    def observe(self, node: etree._Element) -> bool:
        if node.tag == "noteStmt" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "type")
