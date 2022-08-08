from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class TeiNamespaceObserver(AbstractNodeObserver):
    """Dummy plugin for TEI element

    This observer doen't do anything, action is performed in TeiTransformer.
    Use this as plugin anyway, if you want to add xml namespace for TEI
    (http://www.tei-c.org/ns/1.0) to a file."""

    def observe(self, node: etree._Element) -> bool:
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
