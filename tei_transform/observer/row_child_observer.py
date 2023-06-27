from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class RowChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> children of <row/>.

    Find <p/> elements that are direct children of <row/> and wrap
    them in a new <cell/> element.
    If the element is empty (i.e. it contains no text, tail, or has
    no children), it is removed instead.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "row":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            parent.remove(node)
        else:
            new_cell = create_new_element(node, "cell")
            element_index = parent.index(node)
            parent.insert(element_index, new_cell)
            new_cell.append(node)
