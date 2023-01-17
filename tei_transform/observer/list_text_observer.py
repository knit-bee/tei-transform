from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class ListTextObserver(AbstractNodeObserver):
    """
    Observer for <list/> elements that contain text.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if node.text is not None and node.text.strip():
                return True
            # check if  any <item/> has tail
            if [
                child for child in node if child.tail is not None and child.tail.strip()
            ] != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
