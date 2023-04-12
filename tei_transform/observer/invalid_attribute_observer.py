import logging
from typing import Dict, Optional, Set

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node

logger = logging.getLogger(__name__)


class InvalidAttributeObserver(AbstractNodeObserver):
    """
    Observer for elements with invalid attributes.

    Remove defined attributes from all elements unless element
    tag is marked as exception.
    This requires configuration by setting the target attributes
    and, if any, the exceptions where the attribute should not
    be removed.
    """

    def __init__(self, target_attributes: Optional[Dict[str, Set[str]]] = None) -> None:
        """
        To instantiate, pass a dictionary where the keys are the target
        attributes and the values are sets containing the localnames of
        elements from which the corresponding attribute should not be
        removed. If an attribute should be removed globally, pass an empty
        set as value.
        """
        self.target_attributes = target_attributes

    def observe(self, node: etree._Element) -> bool:
        if self.target_attributes is not None:
            matching_attributes = set(self.target_attributes).intersection(node.attrib)
            for match in matching_attributes:
                if etree.QName(node).localname not in self.target_attributes[match]:
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        for target_attr, elements in self.target_attributes.items():
            if etree.QName(node).localname not in elements:
                remove_attribute_from_node(node, target_attr)

    def configure(self, config_dict: Dict[str, str]) -> None:
        target_attributes = {
            key: {elem.strip() for elem in value.split(",") if elem}
            for key, value in config_dict.items()
        }
        if not target_attributes:
            logger.warning("Invalid configuration for InvalidAttributeObserver.")
            return
        self.target_attributes = target_attributes
