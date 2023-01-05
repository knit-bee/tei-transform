from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class EmptyListObserver(AbstractNodeObserver):
    """
    Observer for empty <list/>, <table/>, and <row/> elements.

    Find <list/> elements that don't contain any <item/> elements
    or text, find <table/> elements that don't contain any <row/>
    elements or text and remove them; find <row/> elements that
    don't contain any <cell/> elements or text and remove them.

    If the target element has a non-whitespace tail, it will be added,
    for <list/> and <table/> elements, as text content of a new <p/>
    element that is inserted at the index of the target element. For
    empty <row/> elements with tail, a new <cell/> element is added
    as a child with the tail of the <row/> as text content (i.e. the
    <row/> is now not empty and thus not removed).
    N.B.: If the any of the possible target elements contains text,
    they are not considered empty and thus not handled. However, the
    tree would be still not valid TEI and another transformation
    should be applied.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"list", "row", "table"}:
            if len(node) == 0 and (node.text is None or not node.text.strip()):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if etree.QName(node).localname == "row":
            self._handle_row(node, parent)
        else:
            self._handle_list_or_table(node, parent)

    def _handle_row(self, node: etree._Element, parent: etree._Element) -> None:
        if node.tail and node.tail.strip():
            new_cell = create_new_element(node, "cell")
            new_cell.text = node.tail
            node.tail = None
            node.append(new_cell)
        else:
            parent.remove(node)
            if self.observe(parent):
                self.transform_node(parent)

    def _handle_list_or_table(
        self, node: etree._Element, parent: etree._Element
    ) -> None:
        if node.tail and node.tail.strip():
            tail_text = node.tail
            new_p = create_new_element(node, "p")
            new_p.text = tail_text
            parent_tag = etree.QName(parent).localname
            if parent_tag in {"p", "item", "cell", "ab", "fw", "quote", "head"}:
                if parent.text:
                    parent.text += " " + tail_text
                else:
                    parent.text = tail_text
            else:
                node.addnext(new_p)
        parent.remove(node)
