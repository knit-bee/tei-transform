import os
import shutil
from typing import Protocol

from lxml import etree


class XmlWriter(Protocol):
    def write_xml(self, path: str, xml: etree._Element) -> None:
        ...

    def create_output_directories(self, output_dir: str) -> None:
        ...

    def copy_valid_files(self, file: str, output_dir: str) -> None:
        ...


class XmlWriterImpl:
    def write_xml(self, path: str, xml: etree._Element) -> None:
        if xml is not None:
            xml.getroottree().write(
                path,
                xml_declaration=True,
                encoding="utf-8",
            )

    def create_output_directories(self, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)

    def copy_valid_files(self, file: str, output_dir: str) -> None:
        shutil.copy2(file, output_dir)
