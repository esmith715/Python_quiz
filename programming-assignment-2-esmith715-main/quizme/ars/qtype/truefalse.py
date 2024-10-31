from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from typing import Optional, Any
from .question import Question

"""Module for the TrueFalse quiz item class in the Adaptive Review System."""

class TrueFalse(Question):
    """Class for a True/False quiz item."""

    def __init__(self, question: str, answer: bool, explanation: str = ""):
        """Initialize a true/false quiz item.
        
        Args:
            question (str): The question to be displayed.
            answer (bool): The correct answer, either True or False.
            explanation (str, optional): Additional information to explain the correct answer.
        
        Raises:
            ValueError: If the answer is not a boolean.
        """
        super().__init__(question, answer)
        if not isinstance(answer, bool):
            raise ValueError("The answer must be a boolean (True or False).")
        self._explanation = explanation

    def ask(self) -> str:
        """Return the true/false question text.
        
        Returns:
            str: The text of the question followed by " (True/False)".
        """
        self._last_asked = datetime.now()
        return f"{self._question} (True/False)"

    def check_answer(self, answer: str) -> bool:
        """Check if the provided answer is correct.
        
        Args:
            answer (str): The user's answer to the question.
        
        Returns:
            bool: True if the answer is correct, False otherwise.
        
        Raises:
            ValueError: If the answer is not 'True' or 'False'.
        """
        normalized_answer = answer.strip().lower()
        if normalized_answer in ["true", "t"]:
            user_answer = True
        elif normalized_answer in ["false", "f"]:
            user_answer = False
        else:
            raise ValueError("Answer must be 'True' or 'False'.")
        return user_answer == self._answer

    def incorrect_feedback(self) -> str:
        """Return feedback for an incorrect answer.
        
        Returns:
            str: Feedback message for an incorrect answer, including the explanation if provided.
        """
        feedback = "Incorrect. "
        if self._explanation:
            feedback += f"{self._explanation}"
        return feedback

    def __eq__(self, other: object) -> bool:
        """Define equality based on the question's unique id.
        
        Args:
            other (object): The object to compare with.
        
        Returns:
            bool: True if the other object is a Question with the same id, False otherwise.
        """
        if isinstance(other, TrueFalse):
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
        return f"TrueFalse(id={self._id}, question={self._question}, last_asked={self._last_asked})"
