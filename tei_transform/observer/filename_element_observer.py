from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class FilenameElementObserver(AbstractNodeObserver):
    """
    Observer for <filename/> elements.

    Find <filename/> elements and remove them.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "filename":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        parent.remove(node)
