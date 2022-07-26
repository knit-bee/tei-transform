import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class RevisionDescChange:
    person: List[str]
    date: datetime.date
    reason: str
