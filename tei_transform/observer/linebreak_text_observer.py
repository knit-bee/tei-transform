from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class LinebreakTextObserver(AbstractNodeObserver):
    """
    Observer for <lb/> elements that contain text.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "lb"
            and node.text is not None
            and node.text.strip()
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
