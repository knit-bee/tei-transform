import logging
from typing import Dict, Optional, Set

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class InvalidAttributeObserver(AbstractNodeObserver):
    """
    Observer for elements with invalid attributes.

    """

    def __init__(self, target_attributes: Optional[Dict[str, Set[str]]] = None) -> None:
        self.target_attributes = target_attributes

    def observe(self, node: etree._Element) -> bool:
        if self.target_attributes is not None:
            matching_attributes = set(self.target_attributes).intersection(node.attrib)
            for match in matching_attributes:
                if etree.QName(node).localname in self.target_attributes[match]:
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass

    def configure(self, config_dict: Dict[str, str]) -> None:
        target_attributes = {
            key: {elem.strip() for elem in value.split(",") if elem}
            for key, value in config_dict.items()
        }
        if not target_attributes:
            logger.warning("Invalid configuration for InvalidAttributeObserver.")
            return
        self.target_attributes = target_attributes
