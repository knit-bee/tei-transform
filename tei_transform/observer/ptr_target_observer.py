from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class PtrTargetObserver(AbstractNodeObserver):
    """
    Observer for <ptr/> elements with emtpy @target attribute
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "ptr"
            and node.attrib.get("target", None) == ""
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
