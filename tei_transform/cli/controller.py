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
            description="""Parse xml-files that have some errors (that make them
            invalid according to TEI P5) and apply transformations to the file
            content and save to new file. The old file is not changed.
            There are options to validate files before processing to e.g.
            ignore valid files. Files are validated against the Relax NG scheme
            of the current version of  the TEI guidelines (tei_all.rng)."""
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
            "--revision-config",
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
        valid_file_handling_group = parser.add_mutually_exclusive_group()
        valid_file_handling_group.add_argument(
            "--no-validation",
            action="store_true",
            help="""Do not validate files before processing. This is the default
            setting. Valid files will be written to output directory with new
            timestamp but without changes to the xml tree. An xml-declaration
            is added as default and the formatting of the document may change.""",
        )
        valid_file_handling_group.add_argument(
            "--copy-valid",
            action="store_true",
            help="""Validate files before processing and copy valid files from
            input directory to output directory, trying to preserve metadata
            (i.e. timestamps are preserved, permissions if possible). """,
        )
        valid_file_handling_group.add_argument(
            "--ignore-valid",
            action="store_true",
            help="""Validate files before processing and ignore valid file during
            processing. Only transformed files are written to the output directory.""",
        )
        args = parser.parse_args(arguments)
        validation = not (args.no_validation) and any(
            [args.copy_valid, args.ignore_valid]
        )
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
                validation=validation,
                copy_valid=args.copy_valid,
            )
        )
