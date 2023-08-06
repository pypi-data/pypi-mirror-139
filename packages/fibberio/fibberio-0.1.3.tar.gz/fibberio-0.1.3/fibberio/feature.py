from .source import Source
from .distribution import Distribution


class Feature:
    def __init__(self) -> None:
        self.target: list[str] = []
        self.source: Source = None
        self.distribution: Distribution = None

    def validate(self) -> bool:
        return True
