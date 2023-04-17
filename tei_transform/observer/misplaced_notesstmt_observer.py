from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MisplacedNotesstmtObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "notesStmt":
            prev_sibling = node.getprevious()
            if (
                prev_sibling is not None
                and etree.QName(prev_sibling).localname == "sourceDesc"
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
