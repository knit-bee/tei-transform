from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class TableChildObserver(AbstractNodeObserver):
    """
    Observer for invalid children of <table/>.

    Find <p/> elements that are children of <table/> and change
    their tag to <fw/>. If the element is empty, it is removed
    instead.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "table":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
