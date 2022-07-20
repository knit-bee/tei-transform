import argparse
from typing import List

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCase


class TeiTransformController:
    def __init__(self, use_case: TeiTransformationUseCase) -> None:
        self.use_case = use_case

    def process_arguments(self, arguments: List[str]) -> None:
        pass
