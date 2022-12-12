from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class TailTextObserver(AbstractNodeObserver):
    """
    Observer for elements with text in tail.

    Search for elements with tags <p>, <fw> or <ab> that
    are descendants of <text> and contain text in their tail.
    The text in the element tail will be removed and added to
    a new sibling element with tag <p>.
    """

    def observe(self, node: etree._Element) -> bool:
        node_local_tag = etree.QName(node).localname
        if node_local_tag in {"p", "ab"}:
            # check that node appears in <text> not in <teiHeader>
            if list(node.iterancestors("{*}text")) != []:
                if node.tail is not None and node.tail.strip():
                    return True
        elif node_local_tag == "fw":
            ancestor_tags = [
                etree.QName(parent.tag).localname
                for parent in node.iterancestors(["{*}text", "{*}p"])
            ]
            if "text" in ancestor_tags:
                # tail text in <fw> is allowed if parent is <p>
                if "p" in ancestor_tags:
                    return False
                if node.tail is not None and node.tail.strip():
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        tail_text = node.tail
        new_elem = create_new_element(node, "p")
        new_elem.text = tail_text
        node.tail = None
        node.addnext(new_elem)
