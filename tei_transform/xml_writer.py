import os
from typing import Protocol

from lxml import etree


class XmlWriter(Protocol):
    def write_xml(self, path: str, xml: etree._Element) -> None:
        ...

    def create_output_directories(self, file_path: str) -> None:
        ...


class XmlWriterImpl:
    def write_xml(self, path: str, xml: etree._Element) -> None:
        if xml is not None:
            xml.getroottree().write(
                path,
                xml_declaration=True,
                encoding="utf-8",
            )

    def create_output_directories(self, file_path: str) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
