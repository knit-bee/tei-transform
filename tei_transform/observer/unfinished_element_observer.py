from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class UnfinishedElementObserver(AbstractNodeObserver):
    """
    Observer for non-empty <list/> and <table/> elements that are
    missing required children.

    """

    def observe(self, node: etree._Element) -> bool:
        element_tag = etree.QName(node).localname
        if element_tag == "list" and len(node) != 0:
            if list(node.iterchildren("{*}item")) == []:
                return True
        if element_tag == "table" and len(node) != 0:
            if list(node.iterchildren("{*}row")) == []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if etree.QName(node).localname == "list":
            self._handle_list(node)
        if etree.QName(node).localname == "table":
            self._handle_table(node)

    def _handle_list(self, node: etree._Element) -> None:
        new_item = create_new_element(node, "item")
        insert_index = 0
        for child in node.iterchildren(["{*}head", "{*}desc"], reversed=True):
            insert_index = node.index(child) + 1
            break
        node.insert(insert_index, new_item)

    def _handle_table(self, node: etree._Element) -> None:
        new_row = create_new_element(node, "row")
        new_cell = create_new_element(node, "cell")
        insert_index = 0
        for child in node.iterchildren("{*}head", reversed=True):
            insert_index = node.index(child) + 1
            break
        new_row.append(new_cell)
        node.insert(insert_index, new_row)
