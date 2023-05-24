from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class MissingPublisherObserver(AbstractNodeObserver):
    """
    Observer for <publicationStmt> elements that are missing <publisher/>.

    Find empty <publicationStmt/> elements or <publicationStmt/> elements
    that are missing an element from the publicationStmtPart.agency group
    (i.e. <publisher/>, <authority/>, <distributor/>). If none of these
    elements is present an empty <publisher/> element is inserted as first
    child of the <publicationStmt/> element. If all children are <p/> or
    <ab/>, no <publisher/> is added.
    N.B.: This will only check if any of the required tags is present, not
    if they also appear as first child of <publicationStmt/>.
    """

    # cf. https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.publicationStmtPart.agency.html
    pub_stmt_agency_tags = {"publisher", "authority", "distributor"}

    def observe(self, node: etree._Element) -> bool:
        # empty <publicationStmt/>
        if etree.QName(node).localname == "publicationStmt" and len(node) == 0:
            return True
        # check first child of <publicationStmt>
        parent = node.getparent()
        if (
            parent is not None
            and etree.QName(parent).localname == "publicationStmt"
            and parent.index(node) == 0
        ):
            child_tags = [etree.QName(child).localname for child in parent]
            # if all children are pLike, no <publisher/> is needed
            if all(tag in {"p", "ab"} for tag in child_tags):
                return False
            # otherwise, check if any child is from the publicationStmtPart.agency group
            if not any(tag in self.pub_stmt_agency_tags for tag in child_tags):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if etree.QName(node).localname == "publicationStmt":
            target = node
        else:
            target = node.getparent()
        empty_publisher = create_new_element(node, "publisher")
        target.insert(0, empty_publisher)
