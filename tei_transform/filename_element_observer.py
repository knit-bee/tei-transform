from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class FilenameElementObserver(AbstractNodeObserver):
    xpattern = "//filename"

    def observe(self, node: etree._Element) -> bool:
        if node.tag == "filename":
            return True
        return False
