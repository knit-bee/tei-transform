from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivParentObserver(AbstractNodeObserver):
    """
    Observer for <div/> elements with invalid parent.

    Find <div/> elements that are not descendants of <body/>, <back/>,
    <front/> or other <div/> elements or <lem/> or <rdg/>.
    If the tag of the parent element is <p/> or <ab/> and the target
    <div/> element has children, the <div/> element is added as a
    following sibling of the former parent. Any elements that were
    siblings of <div/> in the <p/>-like element are added with a new
    parent with the same tag as the old parent under a <div/> that
    is added as sibling of the target <div/>. If the target <div/>
    has a tail, it is added as text content of a new <p/> which is
    appended to the <div/>.
    For all other tags or if the <div/> element has no descendants,
    the invalid <div/> element will be stripped from the tree by
    merging its children, text and tail into the parent element.

    N.B. This transformation might result in an invalid tree, e.g.
    if the parent has other <p/> as siblings. Use in combination with
    pluings that handle invalid siblings of <div/>.
    """

    def observe(self, node: etree._Element) -> bool:
        valid_div_parents = {"div", "body", "lem", "rdg", "back", "front"}
        if etree.QName(node).localname == "div":
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname not in valid_div_parents
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        p_like_tags = {"p", "ab"}
        parent = node.getparent()
        parent_tag = etree.QName(parent).localname
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            parent.remove(node)
            return
        if parent_tag in p_like_tags and len(node) != 0:
            self._handle_element_with_plike_parent(node, parent, parent_tag)
            return
        # element without children or parent not <p/> or <ab/>
        node.tag = "tempRename"
        etree.strip_tags(parent, "tempRename")

    def _handle_element_with_plike_parent(
        self, element: etree._Element, parent: etree._Element, parent_tag: str
    ) -> None:
        following_siblings = list(element.itersiblings())
        grand_parent = parent.getparent()
        parent_index = grand_parent.index(parent)
        if following_siblings:
            new_plike = create_new_element(element, parent_tag)
            new_plike.extend(following_siblings)
            new_div = create_new_element(element, "div")
            new_div.append(new_plike)
            grand_parent.insert(parent_index + 1, new_div)
        grand_parent.insert(parent_index + 1, element)
        if element.tail is not None and element.tail.strip():
            self._add_tail_of_div_element_to_new_p(element)

    def _add_tail_of_div_element_to_new_p(self, element: etree._Element) -> None:
        new_p = create_new_element(element, "p")
        new_p.text = element.tail.strip()
        element.tail = None
        element.append(new_p)
