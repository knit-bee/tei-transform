from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class EmptyListObserver(AbstractNodeObserver):
    """
    Observer for empty <list/> elements.

    Find <list/> elements that don't contain any <item/> elements
    or text and remove them.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if not len(node) and (node.text is None or not node.text.strip()):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        parent.remove(node)


# TODO: how to handle tail on empty list?
# add to parent? > not possible if parent <div>
