from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class WrongListChildObserver(AbstractNodeObserver):
    """
    Observer for <p/>, <hi/>, and <ab/> elements with <list/> parent.

    Find <p/>, <hi/>, and <ab/> elements that are direct children of
    <list/> and wrap them with a new <item/> element.
    If the target element is empty (i.e. doesn't contain text, tail,
    or children), it will be removed instead.
    """

    def observe(self, node: etree._Element) -> bool:
        target_tags = {"p", "hi", "ab"}
        if etree.QName(node).localname in target_tags:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "list":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
