from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class FilenameElementObserver(AbstractNodeObserver):
    """
    Observer for <filename/> nodes.

    Find <filename/> elements and replace their tags with <idno/>
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "filename":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "notesStmt")
        info = node.text
        child_tag = etree.QName(node.nsmap.get(None, None), "note")
        child = etree.Element(child_tag.text)
        child.set("type", "filename")
        child.text = info
        node.text = None
        node.append(child)
