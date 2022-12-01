from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MissingPublisherObserver(AbstractNodeObserver):
    """
    Observer for <publicationStmt> elements that are missing <publisher/>.

    Find empty <publicationStmt/> elements or <publicationStmt/> elements
    that are missing an element from the publicationStmtPart.agency group
    (i.e. <publisher/>, <authority/>, <distributor/>). If none of these
    elements is present an empty <publisher/> element is inserted as first
    child of the <publicationStmt/> element. N.B.: This will only check if
    any of the required tags is present, not if they also appear as first
    child of <publicationStmt/>.
    """

    # cf. https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.publicationStmtPart.agency.html
    pub_stmt_agency_tags = {"publisher", "authority", "distributor"}

    def observe(self, node: etree._Element) -> bool:
        # empty <publicationStmt/>
        if etree.QName(node).localname == "publicationStmt" and len(node) == 0:
            return True
        # check first child of <publicationStmt> if there are siblings
        # from the publicationStmtPart.agency group
        parent = node.getparent()
        if parent is not None and etree.QName(parent).localname == "publicationStmt":
            if parent.index(node) == 0 and not [
                child
                for child in parent
                if etree.QName(child).localname in self.pub_stmt_agency_tags
            ]:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
