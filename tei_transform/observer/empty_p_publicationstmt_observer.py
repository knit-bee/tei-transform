from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.observer.observer_errors import ManualCurationNeeded


class EmptyPPublicationstmtObserver(AbstractNodeObserver):
    """
    Observer for p-like elements that are children of <publicationStmt/>.
    """

    def observe(self, node: etree._Element) -> bool:
        target_tags = {"p", "ab"}
        if etree.QName(node).localname in target_tags:
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname == "publicationStmt"
            ):
                if any(
                    etree.QName(child).localname not in target_tags for child in parent
                ):
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            parent = node.getparent()
            parent.remove(node)
        else:
            raise ManualCurationNeeded()
