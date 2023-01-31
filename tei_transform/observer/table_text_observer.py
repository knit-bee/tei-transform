from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


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
        pass
