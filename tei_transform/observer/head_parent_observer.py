from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class HeadParentObserver(AbstractNodeObserver):
    """
    Observer for <head/> elements with <p/>, <ab/>, <head/>, <hi/>
    or <item/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "head":
            parent = node.getparent()
            if etree.QName(parent).localname in {"p", "ab", "head", "hi", "item"}:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
