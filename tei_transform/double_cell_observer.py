from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class DoubleCellObserver(AbstractNodeObserver):
    """
    Observer for <cell/> elements that are children of <cell/>

    Find <cell/> elements that are children of <cell/> and change
    its tag to <p> if it has no children. If the inner <cell/> has
    children, it is added as a sibling before the outer cell.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "cell":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "cell":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if not node.getchildren():
            change_element_tag(node, "p")
            node.attrib.pop("role", None)
        else:
            # Adding the inner cell before the outer might break the
            # order of the table. Assuming, however, that it is already
            # broken, it seems a good enough solution to resolve the
            # problem of <cell/> elements in other <cell/>.
            parent = node.getparent()
            parent.addprevious(node)
