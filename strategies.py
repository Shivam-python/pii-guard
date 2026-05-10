import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    value: str
    start: int
    end: int


class BaseStrategy:
    def apply(self, text: str) -> str:
        raise NotImplementedError


class RegexStrategy(BaseStrategy):
    def __init__(self, pattern, replacement="[REDACTED]"):
        self.pattern = pattern
        self.replacement = replacement

    def apply(self, text: str) -> str:
        return self.pattern.sub(self.replacement, text)

    def find_matches(self, text: str) -> List[MatchResult]:
        matches = []

        for match in self.pattern.finditer(text):
            matches.append(
                MatchResult(
                    value=match.group(),
                    start=match.start(),
                    end=match.end(),
                )
            )

        return matches
