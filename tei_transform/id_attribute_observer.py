from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class IdAttributeObserver(AbstractNodeObserver):
    xpattern = "//*[@id]"

    def observe(self, node: etree._Element) -> bool:
        if "id" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
