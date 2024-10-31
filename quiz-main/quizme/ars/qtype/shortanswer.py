import re
from datetime import datetime
from typing import Optional
from .question import Question

"""Module for the ShortAnswer quiz item class in the Adaptive Review System."""

class ShortAnswer(Question):
    """A quiz item representing a short answer question."""

    def __init__(self, question: str, answer: str, case_sensitive: bool = False):
        """Initialize a short answer quiz item.
        
        Args:
            question (str): The question prompt.
            answer (str): The correct answer.
            case_sensitive (bool, optional): Whether the answer comparison should be case-sensitive. Defaults to False.
        """
        super().__init__(question, answer)
        self._case_sensitive = case_sensitive

    def _normalize(self, text: str) -> str:
        """Normalize the text for comparison.
        
        Args:
            text (str): The text to normalize.
        
        Returns:
            str: The normalized text.
        """
        text = text.strip()
        if not self._case_sensitive:
            text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def check_answer(self, answer: str) -> bool:
        """Check if the provided answer is correct.
        
        Args:
            answer (str): The provided answer.
        
        Returns:
            bool: True if the provided answer is correct, False otherwise.
        """
        normalized_provided_answer = self._normalize(answer)
        normalized_correct_answer = self._normalize(self._answer)
        return normalized_provided_answer == normalized_correct_answer

    def incorrect_feedback(self) -> str:
        """Return feedback for an incorrect answer.
        
        Returns:
            str: Feedback message for an incorrect answer.
        """
        return f"Incorrect. The correct answer is: {self._answer}"

    def ask(self) -> str:
        """Return the short answer question text.
        
        Returns:
            str: The text of the question.
        """
        self._last_asked = datetime.now()
        return self._question

    def __eq__(self, other: object) -> bool:
        """Define equality based on the question's unique id.
        
        Args:
            other (object): The object to compare with.
        
        Returns:
            bool: True if the other object is a Question with the same id, False otherwise.
        """
        if isinstance(other, ShortAnswer):
            return self._id == other.id
        return False

    def __hash__(self) -> int:
        """Define a hash value based on the question's unique id.
        
        Returns:
            int: Hash value of the question's unique id.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """Return a string representation of the Question object."""
        return f"ShortAnswer(id={self._id}, question={self._question}, last_asked={self._last_asked})"
