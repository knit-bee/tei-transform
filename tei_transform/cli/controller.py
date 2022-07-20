import argparse
from typing import List

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCase


class TeiTransformController:
    def __init__(self, use_case: TeiTransformationUseCase) -> None:
        self.use_case = use_case

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(
            description="""Parse an xml-file that has some errors (that make it
            invalid according to TEI P5) and apply transformations the file
            content."""
        )
        parser.add_argument(
            "file",
            help="File to process",
            type=str,
        )
        parser.add_argument(
            "--transformation",
            "-t",
            help="""Observer plugins that should be used to transform the file
            content. If no plugin is passed, the default setting will be used
            ('schemalocation, id-attribute, teiheader, notestmt, filename-element')""",
            nargs="+",
            default=[
                "schemalocation",
                "id-attribute",
                "teiheader",
                "notestmt",
                "filename-element",
            ],
        )
        args = parser.parse_args(arguments)
        self.use_case.process(CliRequest(file=args.file, observers=args.transformation))
