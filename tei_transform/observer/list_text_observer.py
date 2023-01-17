from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


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
        if node.text is not None and node.text.strip():
            new_item = create_new_element(node, "item")
            new_item.text = node.text.strip()
            node.text = None
            node.insert(0, new_item)
        for child in node.iter():
            if child.tail is not None and child.tail.strip():
                new_item = create_new_element(node, "item")
                new_item.text = child.tail.strip()
                child.tail = None
                node.insert(node.index(child) + 1, new_item)
