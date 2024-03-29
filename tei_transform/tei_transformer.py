import logging
from typing import List, Optional, Tuple

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import construct_new_tei_root
from tei_transform.observer import TeiNamespaceObserver
from tei_transform.observer.observer_errors import TransformationError
from tei_transform.parse_config import RevisionDescChange
from tei_transform.xml_tree_iterator import XMLTreeIterator

logger = logging.getLogger(__name__)


class TeiTransformer:
    """Apply transformation specified by node observers to xml tree"""

    def __init__(
        self,
        xml_iterator: XMLTreeIterator,
    ):
        self.xml_iterator = xml_iterator
        self._first_pass_observers: List[AbstractNodeObserver]
        self._second_pass_observers: List[AbstractNodeObserver]
        self._xml_changed: bool = False

    def set_list_of_observers(
        self,
        lists_of_observers: Tuple[
            List[AbstractNodeObserver], List[AbstractNodeObserver]
        ],
    ) -> None:
        self._first_pass_observers, self._second_pass_observers = lists_of_observers

    def perform_transformation(self, filename: str) -> etree._Element:
        """
        Iterate over file and apply transformations defined by
        observers to the xml tree.
        """
        self._xml_changed = False
        transformed_nodes = []
        try:
            for node in self.xml_iterator.iterate_xml(filename):
                self._transform_subtree_of_node(
                    node, self._first_pass_observers, filename
                )
                self._transform_subtree_of_node(
                    node, self._second_pass_observers, filename
                )
                transformed_nodes.append(node)
        except etree.XMLSyntaxError:
            logger.exception("File ignored: %s" % filename)
            return None
        if any(
            isinstance(observer, TeiNamespaceObserver)
            for observer in self._first_pass_observers
        ):
            new_root = construct_new_tei_root(
                transformed_nodes[0], ns_to_add={None: "http://www.tei-c.org/ns/1.0"}
            )
            transformed_nodes[0] = new_root
        root = self._construct_element_tree(transformed_nodes)
        if root is None:
            logger.warning("No 'TEI' element found, file ignored: %s" % filename)
        return root

    def xml_tree_changed(self) -> bool:
        """Check if any transformation was applied by an observer."""
        return self._xml_changed

    def add_change_to_revision_desc(
        self, tree: etree._Element, change: RevisionDescChange
    ) -> None:
        """
        Add entry to <revisionDesc/> in <teiHeader> to document changes
        applied to the document. If no <revisionDesc/> is contained in the
        document, if will be created and added.
        """
        ns_prefix = tree.nsmap.get(None, None)
        new_change = etree.Element(
            etree.QName(ns_prefix, "change"), {"when": change.date}
        )
        for person_name in change.person:
            name_node = etree.Element(etree.QName(ns_prefix, "name"))
            name_node.text = person_name
            new_change.append(name_node)
        if len(new_change) > 0:
            new_change[-1].tail = change.reason
        else:
            new_change.text = change.reason

        revision_node = tree.find(".//{*}revisionDesc")
        if revision_node is None:
            self._add_revision_desc_to_tei_header(tree, new_change, ns_prefix)
        else:
            revision_node.append(new_change)
        return tree

    def _add_revision_desc_to_tei_header(
        self, tree: etree._Element, new_change: etree._Element, ns_prefix: str
    ) -> None:
        revision_node = etree.Element(etree.QName(ns_prefix, "revisionDesc"))
        revision_node.append(new_change)
        # add revisionDesc as last child of teiHeader if not present
        teiheader = tree.find(".//{*}teiHeader")
        if teiheader is not None:
            teiheader.append(revision_node)

    def _transform_subtree_of_node(
        self,
        node: etree._Element,
        list_of_observers: List[AbstractNodeObserver],
        filename: str,
    ) -> None:
        for subnode in node.iter():
            for observer in list_of_observers:
                if observer.observe(subnode):
                    try:
                        observer.transform_node(subnode)
                    except TransformationError:
                        logger.exception("Manual curation needed: file %s" % filename)
                    else:
                        self._xml_changed = True

    def _construct_element_tree(
        self, list_of_nodes: List[etree._Element]
    ) -> Optional[etree._Element]:
        if list_of_nodes:
            first_node = etree.QName(list_of_nodes[0].tag)
            if first_node.localname == "TEI":
                root = list_of_nodes[0]
                root.extend(list_of_nodes[1:])
                return root
        return None
