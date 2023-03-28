from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class RespStmtNoteObserver(AbstractNodeObserver):
    """
    Observer for <note/> elements in <respStmt/>.

    Find <note/> elements with <respStmt/> parent that have
    no <resp/> sibling before. Wrap the <note/> element in
    a new <resp/> element.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "note":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "respStmt":
                if list(node.itersiblings("{*}resp", preceding=True)) == []:
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_resp = create_new_element(node, "resp")
        parent = node.getparent()
        note_index = parent.index(node)
        parent.insert(note_index, new_resp)
        new_resp.append(node)
