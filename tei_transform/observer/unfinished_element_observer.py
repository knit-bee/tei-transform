from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


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
        pass
