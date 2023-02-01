from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


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
        pass
