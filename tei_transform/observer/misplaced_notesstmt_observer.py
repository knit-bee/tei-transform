from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MisplacedNotesstmtObserver(AbstractNodeObserver):
    """
    Observer for <notesStmt/> that follow <sourceDesc/>.

    Find <notesStmt/> elements with <sourceDesc/> as
    older sibling and insert the <notesStmt/> element
    before the <sourceDesc/>.
    If the <notesStmt/> element has no children, it is
    removed.
    """

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
        if len(node) == 0:
            node.getparent().remove(node)
        else:
            first_source_desc_sibling = node.getparent().find("{*}sourceDesc")
            first_source_desc_sibling.addprevious(node)
