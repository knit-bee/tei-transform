import os
from dataclasses import dataclass
from typing import List, Optional, Protocol

from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.revision_desc_change import (
    RevisionDescChange,
    construct_change_from_config_file,
)
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_writer import XmlWriter


@dataclass
class CliRequest:
    file_or_dir: str
    observers: List[str]
    config: Optional[str] = None
    output: str = "output"


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

    def process(self, request: CliRequest) -> None:
        """
        Processes cli arguments and applies them to the transformation
        of an xml tree.
        """
        observer_list = self.observer_constructor.construct_observers(request.observers)
        self.tei_transformer.set_list_of_observers(observer_list)
        change = None
        if request.config is not None:
            change = construct_change_from_config_file(request.config)
        if os.path.isfile(request.file_or_dir):
            self._process_file(
                file=request.file_or_dir,
                output_dir=request.output,
                revision_entry=change,
            )
        elif os.path.isdir(request.file_or_dir):
            for root, dirs, files in os.walk(request.file_or_dir):
                for file in files:
                    self._process_file(
                        file=os.path.join(root, file),
                        output_dir=request.output,
                        revision_entry=change,
                    )

    def _process_file(
        self,
        file: str,
        output_dir: str,
        revision_entry: Optional[RevisionDescChange] = None,
    ) -> None:
        new_root = self.tei_transformer.perform_transformation(file)
        if self.tei_transformer.xml_tree_changed() and revision_entry is not None:
            self.tei_transformer.add_change_to_revision_desc(new_root, revision_entry)
        self.xml_writer.write_xml(output_dir, new_root)
