import configparser
import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RevisionDescChange:
    person: List[str]
    date: str
    reason: str
