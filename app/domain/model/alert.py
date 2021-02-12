from dataclasses import dataclass


@dataclass
class Alert:
    id: int
    message: str
    time: str
