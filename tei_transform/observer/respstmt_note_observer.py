from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class RespStmtNoteObserver(AbstractNodeObserver):
    """
    Observer for <note/> elements in <respStmt/>.

    Find <note/> elements with <respStmt/> parent that have invalid
    following sibling (i.e. with tags 'resp', 'name', 'orgName',
    'persName') or with no <resp/> sibling (before or after). Wrap
    the <note/> element in a new <resp/> element.
    """

    def observe(self, node: etree._Element) -> bool:
        parent = node.getparent()
        if (
            parent is not None
            and etree.QName(parent).localname == "respStmt"
            and etree.QName(node).localname == "note"
        ):
            if (
                list(parent.iterchildren("{*}resp")) == []
                or list(
                    node.itersiblings(
                        ["{*}resp", "{*}name", "{*}orgName", "{*}persName"]
                    )
                )
                != []
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_resp = create_new_element(node, "resp")
        parent = node.getparent()
        note_index = parent.index(node)
        parent.insert(note_index, new_resp)
        new_resp.append(node)
