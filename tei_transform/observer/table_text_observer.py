from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    create_new_element,
    merge_text_content,
)


class TableTextObserver(AbstractNodeObserver):
    """
    Observer for <table/> elements that contain text or <p/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "table":
            if node.text is not None and node.text.strip():
                return True
            if [
                child
                for child in node
                if (child.tail is not None and child.tail.strip())
                or etree.QName(child).localname == "p"
            ] != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if node.text is not None and node.text.strip():
            self._handle_text_content_of_table(node)
        for child in node:
            child_tag = etree.QName(child).localname
            if child_tag == "p":
                change_element_tag(child, "fw")
            if child.tail is not None and child.tail.strip():
                if child_tag == "row":
                    self._add_tail_of_row_to_child(child)
                else:
                    if len(child) == 0:
                        child.text = merge_text_content(child.text, child.tail)
                    else:
                        child[-1].tail = merge_text_content(child[-1].tail, child.tail)
                child.tail = None

    def _add_tail_of_row_to_child(self, subnode: etree._Element) -> None:
        if len(subnode) == 0:
            new_cell = create_new_element(subnode, "cell")
            subnode.append(new_cell)
        subnode[-1].text = merge_text_content(subnode[-1].text, subnode.tail)

    def _handle_text_content_of_table(self, node: etree._Element) -> None:
        table_head = create_new_element(node, "head")
        table_head.text = node.text.strip()
        node.text = None
        node.insert(0, table_head)
