from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class FilenameElementObserver(AbstractNodeObserver):
    xpattern = "//filename"

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "filename":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "idno")
