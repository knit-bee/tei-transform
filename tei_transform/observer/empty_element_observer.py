from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class EmptyElementObserver(AbstractNodeObserver):
    """
    Observer for empty <list/>, <table/>, and <row/> elements.

    Find <list/>, <table/>, and <row/> elements that don't contain
    any elements or text and remove them.

    If the target element has a non-whitespace tail, for <list/>
    and <table/> elements, the tail will be concatenated with the
    text of the parent or added as text content of a new <p/> element
    (if the parent shouldn't contain text) that is then inserted
    at the index of the target element. For empty <row/> elements
    with tail, a new <cell/> element is added as a child with the
    tail of the <row/> as text content (i.e. the <row/> is now not
    empty and thus not removed).

    N.B.: If any of the possible target elements contains text,
    they are not considered empty and thus not handled. However, the
    tree would still be invalid TEI and another transformation
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
            if parent is not None:
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
                parent.insert(parent.index(node), new_p)
        parent.remove(node)
