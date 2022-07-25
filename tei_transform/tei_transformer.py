import logging
from typing import List, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.xml_tree_iterator import XMLTreeIterator

logger = logging.getLogger(__name__)


class TeiTransformer:
    def __init__(
        self,
        xml_iterator: XMLTreeIterator,
        list_of_observers: List[AbstractNodeObserver],
    ):
        self.xml_iterator = xml_iterator
        self.list_of_observers = list_of_observers

    def perform_transformation(self, filename: str) -> etree._Element:
        transformed_nodes = []
        try:
            for node in self.xml_iterator.iterate_xml(filename):
                self._transform_subtree_of_node(node)
                transformed_nodes.append(node)
        except etree.XMLSyntaxError:
            logger.info("No elements found in file.")
            return None
        return self._construct_element_tree(transformed_nodes)

    def _transform_subtree_of_node(self, node: etree._Element) -> None:
        for subnode in node.iter():
            for observer in self.list_of_observers:
                if observer.observe(subnode):
                    observer.transform_node(subnode)

    def _construct_element_tree(
        self, list_of_nodes: List[etree._Element]
    ) -> Optional[etree._Element]:
        if list_of_nodes:
            first_node = etree.QName(list_of_nodes[0].tag)
            if first_node.localname == "TEI":
                root = list_of_nodes[0]
                root.extend(list_of_nodes[1:])
                return root
        logger.warning("No 'TEI' element found, no tree constructed.")
        return None
