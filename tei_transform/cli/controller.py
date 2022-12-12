import argparse
from typing import List

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCase


class TeiTransformController:
    """
    Parse command line arguments and pass them to TeiTransformationUseCase
    """

    def __init__(self, use_case: TeiTransformationUseCase) -> None:
        self.use_case = use_case

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(
            description="""Parse an xml-file that has some errors (that make it
            invalid according to TEI P5) and apply transformations the file
            content."""
        )
        parser.add_argument(
            "file_or_dir",
            help="File or directory to process",
            type=str,
        )
        parser.add_argument(
            "--transformation",
            "-t",
            help="""Observer plugins that should be used to transform the file
            content. If no plugin is passed, the default setting will be used
            ('schemalocation, id-attribute, teiheader, notesstmt, filename-element')""",
            nargs="+",
            default=[
                "schemalocation",
                "id-attribute",
                "teiheader",
                "notesstmt",
                "filename-element",
            ],
        )
        parser.add_argument(
            "--revision_config",
            "-c",
            help="""Name of config file where information for change entry for
            revisionDesc element in the teiHeader is stored. If no file is
            passed, no new change entry will be added to revisionDesc.
            The file should contain a section [revision] with the entries 'person =
            Firstname Lastname', 'reason = reason why the file was changed' and
            an optional 'date = YYYY-MM-DD'.
            If the person entry should contain multiple
            names, separate them by comma. If no date parameter is passed,
            the current date will be inserted.""",
            default=None,
        )
        parser.add_argument(
            "--output",
            "-o",
            help="""Name of output directory to store transformed file in. If
            the directory doesn't exist, it will be created. Default is 'output'.""",
            default="output",
        )
        args = parser.parse_args(arguments)
        transformation = []
        for plugin in args.transformation:
            if plugin not in transformation:
                transformation.append(plugin)
        self.use_case.process(
            CliRequest(
                file_or_dir=args.file_or_dir,
                observers=transformation,
                config=args.revision_config,
                output=args.output,
            )
        )
