import os
from typing import Protocol

from lxml import etree


class XmlWriter(Protocol):
    def write_xml(self, path: str, xml: etree._Element) -> None:
        ...


class XmlWriterImpl:
    def write_xml(self, path: str, xml: etree._Element) -> None:
        output_dir = os.path.dirname(path)
        
        if xml is not None:
            xml.getroottree().write(
                path,
                xml_declaration=True,
                encoding="utf-8",
            )
