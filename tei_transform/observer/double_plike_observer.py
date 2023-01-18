from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DoublePlikeObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <ab/> elements with parent <p/> or <ab/>.

    Find <p/> and <ab/> elements that have <p/> or <ab/> as parent
    and strip the inner tag (text and tail as well as the children
    of the inner element will be preserved).
    """

    def observe(self, node: etree._Element) -> bool:
        p_like_tags = {"p", "ab"}
        if etree.QName(node).localname in p_like_tags:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in p_like_tags:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        prev_sibling = node.getprevious()
        last_child = node[-1] if len(node) != 0 else None
        self._pad_text_content_with_whitespace(node)
        node.tag = "tempRename"
        etree.strip_tags(parent, "tempRename")
        # remove multiple whitespace and newline from xml formatting
        self._strip_multiple_whitespaces_from_text_content(parent)
        if prev_sibling is not None:
            self._strip_multiple_whitespaces_from_text_content(prev_sibling, text=False)
        if last_child is not None:
            self._strip_multiple_whitespaces_from_text_content(last_child, text=False)

    def _strip_multiple_whitespaces_from_text_content(
        self, node: etree._Element, text: bool = True
    ) -> None:
        if text is True and node.text is not None:
            node.text = " ".join(node.text.split())
        else:
            if node.tail is not None:
                node.tail = " ".join(node.tail.split())

    def _pad_text_content_with_whitespace(self, node: etree._Element) -> None:
        if node.text is not None:
            node.text = " " + node.text
        if node.tail is not None:
            node.tail = " " + node.tail
