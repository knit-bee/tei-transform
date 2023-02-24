import logging
import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Protocol

from lxml import etree

from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.parse_config import (
    RevisionDescChange,
    construct_change_from_config,
    parse_config_file,
)
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_writer import XmlWriter

logger = logging.getLogger(__name__)


@dataclass
class CliRequest:
    file_or_dir: str
    observers: List[str]
    config: Optional[str] = None
    output: str = "output"
    validation: bool = False
    copy_valid: bool = False
    add_revision: bool = False


class TeiTransformationUseCase(Protocol):
    def process(self, request: CliRequest) -> None:
        ...


@dataclass
class TeiTransformationUseCaseImpl:
    """
    Use case that is called by console script.
    """

    xml_writer: XmlWriter
    tei_transformer: TeiTransformer
    observer_constructor: ObserverConstructor
    tei_scheme: str = ""
    tei_validator: Optional[etree.RelaxNG] = None

    def process(self, request: CliRequest) -> None:
        """
        Processes cli arguments and applies them to the transformation
        of an xml tree.
        """
        observer_lists = self.observer_constructor.construct_observers(
            request.observers
        )
        self.tei_transformer.set_list_of_observers(observer_lists)
        change = None
        if request.config is not None:
            config = parse_config_file(request.config)
        if request.add_revision:
            change = construct_change_from_config(config)
        if request.validation and self.tei_validator is None:
            self._instantiate_tei_validator()
        if os.path.isfile(request.file_or_dir):
            if os.path.splitext(request.file_or_dir)[1] == ".xml":
                self._determine_file_processing_method(
                    file=request.file_or_dir,
                    output_dir=request.output,
                    request=request,
                    revision_entry=change,
                )
        elif os.path.isdir(request.file_or_dir):
            file_or_dir = request.file_or_dir.rstrip(os.sep)
            for root, dirs, files in os.walk(file_or_dir):
                for file in files:
                    if os.path.splitext(file)[1] != ".xml":
                        continue
                    output_dir = output_dir = os.path.join(
                        request.output,
                        os.path.relpath(root, start=os.path.dirname(file_or_dir)),
                    )
                    self._determine_file_processing_method(
                        file=os.path.join(root, file),
                        output_dir=output_dir,
                        request=request,
                        revision_entry=change,
                    )

    def _determine_file_processing_method(
        self,
        file: str,
        output_dir: str,
        request: CliRequest,
        revision_entry: Optional[RevisionDescChange] = None,
    ) -> None:
        self.xml_writer.create_output_directories(output_dir)
        if request.validation:
            assert self.tei_validator is not None
            if self.tei_validator.validate(etree.parse(file)):
                self._process_valid_file(file, output_dir, request.copy_valid)
                return
        self._process_file(file, output_dir, revision_entry)

    def _process_file(
        self,
        file: str,
        output_dir: str,
        revision_entry: Optional[RevisionDescChange] = None,
    ) -> None:
        output_file_path = os.path.join(output_dir, os.path.basename(file))
        new_root = self.tei_transformer.perform_transformation(file)
        if self.tei_transformer.xml_tree_changed() and revision_entry is not None:
            self.tei_transformer.add_change_to_revision_desc(new_root, revision_entry)
        self.xml_writer.write_xml(output_file_path, new_root)

    def _process_valid_file(
        self, file: str, output_dir: str, copy_valid: bool = False
    ) -> None:
        if copy_valid:
            self.xml_writer.copy_valid_files(file, output_dir)

    def _instantiate_tei_validator(self) -> None:
        try:
            self.tei_validator = etree.RelaxNG(etree.parse(self.tei_scheme))
        except OSError:
            sys.exit("Validation scheme file not found.")
        except etree.RelaxNGParseError:
            sys.exit("Invalid scheme.")
        except etree.XMLSyntaxError:
            sys.exit("Invalid xml.")
