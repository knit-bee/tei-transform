from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class MissingBodyObserver(AbstractNodeObserver):
    """
    Observer for <text/> elements missing required children.

    Find <text/> elements that don't have any children with
    tags 'body' or 'group'. A new <body/> element is added
    to the <text/> element and all children of <text/> that
    come between <front/> and <back/>, if present, are added
    as children to the new <body/> element.
    The <body/> element is inserted as first child of <text/>
    or, if a <front/> element is found, after the <front/>
    element.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "text"
            and [
                child
                for child in node
                if etree.QName(child).localname in {"body", "group"}
            ]
            == []
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        body_elem = create_new_element(node, "body")
        front_elem = node.find("{*}front")
        children_to_add = []
        if front_elem is None:
            insert_index = 0
            candidates_to_move = (child for child in node)
        else:
            insert_index = node.index(front_elem) + 1
            candidates_to_move = (sibling for sibling in front_elem.itersiblings())
        for elem in candidates_to_move:
            if etree.QName(elem).localname == "back":
                break
            children_to_add.append(elem)
        node.insert(insert_index, body_elem)
        body_elem.extend(children_to_add)
        # prevent TEI error if body is empty by adding <p/>
        if len(body_elem) == 0:
            new_p = create_new_element(node, "p")
            body_elem.append(new_p)
