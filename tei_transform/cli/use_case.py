import os
from dataclasses import dataclass
from typing import Generator, List, Optional, Protocol, Union

from lxml import etree

from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.revision_desc_change import (
    RevisionDescChange,
    construct_change_from_config_file,
)
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator


@dataclass
class CliRequest:
    file_or_dir: str
    observers: List[str]
    config: Optional[str] = None
    output: Optional[str] = None


class TeiTransformationUseCase(Protocol):
    def process(
        self, request: CliRequest
    ) -> Union[etree._Element, Generator[etree._Element, None, None]]:
        ...


class TeiTransformationUseCaseImpl:
    """
    Use case that is called by console script.
    """

    def process(
        self, request: CliRequest
    ) -> Union[etree._Element, Generator[etree._Element, None, None]]:
        """
        Processes cli arguments and applies them for the transformation
        of an xml tree. The transformed tree is returned.
        """
        tree_iterator = XMLTreeIterator()
        constructor = ObserverConstructor()
        observer_list = constructor.construct_observers(request.observers)
        transformer = TeiTransformer(
            xml_iterator=tree_iterator, list_of_observers=observer_list
        )
        change = None
        if request.config is not None:
            change = construct_change_from_config_file(request.config)
        if request.output is not None:
            os.makedirs(request.output, exist_ok=True)
        if os.path.isfile(request.file_or_dir):
            return self._process_file(
                transformer,
                file=request.file_or_dir,
                output_dir=request.output,
                revision_entry=change,
            )
        elif os.path.isdir(request.file_or_dir):
            for root, dirs, files in os.walk(request.file_or_dir):
                output_sub_dir = None
                if request.output is not None:
                    output_sub_dir = os.path.join(
                        request.output, os.path.relpath(root, start=request.file_or_dir)
                    )
                    os.makedirs(output_sub_dir, exist_ok=True)
                for file in files:
                    self._process_file(
                        transformer,
                        file=os.path.join(root, file),
                        output_dir=output_sub_dir,
                        revision_entry=change,
                    )

    def _process_file(
        self,
        transformer: TeiTransformer,
        file: str,
        output_dir: Optional[str],
        revision_entry: Optional[RevisionDescChange] = None,
    ) -> etree._Element:
        new_root = transformer.perform_transformation(file)
        if transformer.xml_tree_changed() and revision_entry is not None:
            transformer.add_change_to_revision_desc(new_root, revision_entry)
        if output_dir is not None and new_root is not None:
            output_file = os.path.join(output_dir, os.path.basename(file))
            new_root.getroottree().write(
                output_file,
                xml_declaration=True,
                encoding="utf-8",
            )
        return new_root
