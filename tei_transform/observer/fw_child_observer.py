from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class FwChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <list/> elements with <fw/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        target_tags = {"p", "list"}
        if (
            etree.QName(node).localname in target_tags
            and etree.QName(node.getparent()).localname == "fw"
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if etree.QName(node).localname == "p":
            self._handle_p_fw_child(node)
        if etree.QName(node).localname == "list":
            self._handle_list_fw_child(node)

    def _handle_p_fw_child(self, node: etree._Element) -> None:
        parent = node.getparent()
        last_sub_child = node[-1] if len(node) != 0 else None
        prev_sibling = node.getprevious()
        node.tag = "tempRename"
        if node.tail is not None:
            node.tail = " " + node.tail
        if node.text is not None:
            node.text = " " + node.text
        etree.strip_tags(parent, "tempRename")
        if parent.text is not None:
            parent.text = " ".join(parent.text.split())
        if last_sub_child is not None and last_sub_child.tail is not None:
            last_sub_child.tail = " ".join(last_sub_child.tail.split())
        if prev_sibling is not None and prev_sibling.tail is not None:
            prev_sibling.tail = " ".join(prev_sibling.tail.split())

    def _handle_list_fw_child(self, node: etree._Element) -> None:
        change_element_tag(node.getparent(), "ab")
