from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivParentObserver(AbstractNodeObserver):
    """
    Observer for <div/> elements with invalid parent.

    Find <div/> elements that are not descendants of <body/>, <back/>,
    <front/> or other <div/> elements or <lem/> or <rdg/>.
    If the tag of the parent element is <p/> or <ab/>, the parent tag
    will be changed to <div/>, for all other tags the invalid <div/>
    element will be stripped from the tree by merging its children, text
    and tail into the parent element.
    N.B. If the parent element has <p/> or <ab/>, this transformation
    might result in an invalid tree, e.g.:
        - if the parent contains text or children with tail or tags that
            are no valid descendants of <div/>
        - if the parent has e.g. other <p/> as siblings
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
            following_siblings = list(node.itersiblings())
            grand_parent = parent.getparent()
            parent_index = grand_parent.index(parent)
            if following_siblings:
                new_plike = create_new_element(node, parent_tag)
                new_plike.extend(following_siblings)
                new_div = create_new_element(node, "div")
                new_div.append(new_plike)
                grand_parent.insert(parent_index + 1, new_div)
            grand_parent.insert(parent_index + 1, node)
            if node.tail is not None and node.tail.strip():
                new_p = create_new_element(node, "p")
                new_p.text = node.tail.strip()
                node.tail = None
                node.addnext(new_p)
            return
        # element without children or parent not <p/> or <ab/>
        node.tag = "tempRename"
        etree.strip_tags(parent, "tempRename")
