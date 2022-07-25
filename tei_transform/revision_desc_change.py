import datetime
from dataclasses import dataclass


@dataclass
class RevisionDescChange:
    person: str
    date: datetime.date
    reason: str
