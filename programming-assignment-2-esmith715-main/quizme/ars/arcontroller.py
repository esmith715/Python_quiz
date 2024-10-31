"""Core module for running the Adaptive Review System (ARS) session."""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .box import Box
from .boxmanager import BoxManager
from .qtype.shortanswer import ShortAnswer
from .qtype.truefalse import TrueFalse

"""Core module for running the Adaptive Review System (ARS) session."""

class ARController:
    """Main controller for running an adaptive review session."""
    
    def __init__(self, question_data: List[Dict[str, Any]]):
        """Initialize the Adaptive Review Controller.

        Args:
            question_data (List[Dict[str, Any]]): A list of dictionaries containing question data.
        """
        self._box_manager = BoxManager()
        self._initialize_questions(question_data)

    def _initialize_questions(self, question_data: List[Dict[str, Any]]) -> None:
        """Initialize questions and place them in the Unasked Questions box.

        Args:
            question_data (List[Dict[str, Any]]): A list of dictionaries containing question data.
        """
        for q_data in question_data:
            q_type = q_data.get('type')
            try:
                if q_type == 'shortanswer':
                    question = ShortAnswer(
                        question=q_data['question'],
                        answer=q_data['correct_answer'],
                        case_sensitive=q_data.get('case_sensitive', False)
                    )
                elif q_type == 'truefalse':
                    question = TrueFalse(
                        question=q_data['question'],
                        answer=q_data['correct_answer'],
                        explanation=q_data.get('explanation', "")
                    )
                else:
                    print(f"Unsupported question type: {q_type}. Skipping this question.")
                    continue
                self._box_manager.add_new_question(question)
            except KeyError as e:
                print(f"Missing required field for question: {e}. Skipping this question.")

    def start(self) -> None:
        """Run the interactive adaptive review session."""
        print("Type 'q' at any time to quit the session.")

        while True:
            question = self._box_manager.get_next_question()
            if question is None:
                print("All questions have been reviewed. Session complete!")
                break
            
            print(question.ask())
            user_answer = input("Your answer: ")

            if user_answer.lower() == 'q':
                break

            if question.check_answer(user_answer):
                print("Correct!")
                answered_correctly = True
            else:
                print(question.incorrect_feedback())
                answered_correctly = False

            self._box_manager.move_question(question, answered_correctly)
        
        print("Thank you, goodbye!")
