import logging
from dataclasses import dataclass
from typing import List

from transformers import pipeline

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


class NLPModelStrategy(BaseStrategy):
    """
    Uses HuggingFace pii detection model.
    """

    def __init__(
            self,
            entity="PII",
            confidence_threshold=0.75,
    ):
        self.entity = entity
        self.confidence_threshold = confidence_threshold

        self.pipe = pipeline(
            "token-classification",
            model="iiiorg/piiranha-v1-detect-personal-information",
            aggregation_strategy="simple",
        )

    def verify_entity(self, text: str, target: str, expected_entity=None):
        try:
            entities = self.pipe(text)

            for entity in entities:
                entity_text = entity["word"]
                score = entity["score"]

                if target in entity_text and score >= self.confidence_threshold:
                    return True

            return False

        except Exception as e:
            logger.exception("NLP verification failed")
            return False

    def apply(self, text: str) -> str:
        try:
            entities = self.pipe(text)

            entities = sorted(
                entities,
                key=lambda x: x["start"],
                reverse=True,
            )

            for entity in entities:
                if entity["score"] < self.confidence_threshold:
                    continue

                start = entity["start"]
                end = entity["end"]

                replacement = f"[REDACTED_{entity['entity_group']}]"

                text = text[:start] + replacement + text[end:]

            return text

        except Exception:
            logger.exception("NLP masking failed")
            return text


class HybridStrategy(BaseStrategy):
    """
    Regex first.
    NLP fallback only when ambiguity exists.
    """

    def __init__(self, primary, fallback):
        self.regex = primary
        self.nlp = fallback

    def apply(self, text: str) -> str:
        potential_matches = self.regex.find_matches(text)

        if not potential_matches:
            return text
        for match in potential_matches:
            if self._is_ambiguous(match, text):
                is_pii = self.nlp.verify_entity(
                    text=text,
                    target=match.value,
                    expected_entity="PII",
                )

                if is_pii:
                    text = text.replace(
                        match.value,
                        "[REDACTED_PII]",
                    )
                else:
                    logger.debug(
                        "Suppressed false positive: %s",
                        match.value,
                    )
            else:
                text = text.replace(
                    match.value,
                    "[REDACTED_PII]",
                )

        return text

    def _is_ambiguous(self, match, full_text):
        context_window = full_text[
                         max(0, match.start - 25): min(len(full_text), match.end + 25)
                         ].lower()

        ambiguity_keywords = [
            "invoice",
            "txn",
            "transaction",
            "reference",
            "loan",
            "housing",
            "account",
        ]

        return any(keyword in context_window for keyword in ambiguity_keywords)
