from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MissingBodyObserver(AbstractNodeObserver):
    """
    Observer for <text/> elements missing required children.

    Find <text/> elements that don't have any children with
    tags 'body' or 'group'.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "text"
            and [
                child
                for child in node
                if etree.QName(child).localname in {"body", "group"}
            ]
            == []
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
