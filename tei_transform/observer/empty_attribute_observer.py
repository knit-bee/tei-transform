import logging
from typing import Dict, List, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class EmptyAttributeObserver(AbstractNodeObserver):
    """
    Observer for elements with attributes with empty string value.
    """

    def __init__(self, target_attributes: Optional[List[str]] = None) -> None:
        self.target_attributes = target_attributes or []

    def observe(self, node: etree._Element) -> bool:
        pass

    def transform_node(self, node: etree._Element) -> None:
        pass

    def configure(self, config_dict: Dict[str, str]) -> None:
        target_attributes = config_dict.get("target")
        if not target_attributes:
            logger.warning("Invalid configuration for EmptyAttributeObserver.")
            return
        self.target_attributes = target_attributes
