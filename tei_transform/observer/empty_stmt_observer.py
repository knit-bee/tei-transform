from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class EmptyStmtObserver(AbstractNodeObserver):
    """
    Observer for empty <seriesStmt/> and <notesStmt/> elements

    Find <seriesStmt/> and <noteStmt/> elements that don't
    have any children and delete them.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname in {"notesStmt", "seriesStmt"}
            and len(node) == 0
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if parent is not None:
            parent.remove(node)
