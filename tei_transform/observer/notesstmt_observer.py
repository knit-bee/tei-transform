from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class NotesStmtObserver(AbstractNodeObserver):
    """Observer for <notesStmt/> nodes

    Find <notesStmt> elements that have a 'type' attribute
    and remove this attribute from the matching elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "notesStmt" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "type")
