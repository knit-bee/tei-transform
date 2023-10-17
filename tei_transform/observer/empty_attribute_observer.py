import logging
from typing import Dict, Optional, Set

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node

logger = logging.getLogger(__name__)


class EmptyAttributeObserver(AbstractNodeObserver):
    """
    Observer for elements with attributes with empty string value.

    Remove defined attributes from all elements if they have only an empty
    string as value.
    This requires configuration by setting the target attributes.
    """

    def __init__(self, target_attributes: Optional[Set[str]] = None) -> None:
        self.target_attributes = target_attributes or set()

    def observe(self, node: etree._Element) -> bool:
        if self.target_attributes:
            matching_attributes = self.target_attributes.intersection(node.attrib)
            for match in matching_attributes:
                if node.attrib.get(match) == "":
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        for target_attr in self.target_attributes:
            if node.attrib.get(target_attr, None) == "":
                remove_attribute_from_node(node, target_attr)

    def configure(self, config_dict: Dict[str, str]) -> None:
        target_attributes = config_dict.get("target")
        if not target_attributes:
            logger.warning("Invalid configuration for EmptyAttributeObserver.")
            return
        self.target_attributes = {attr.strip() for attr in target_attributes.split(",")}
