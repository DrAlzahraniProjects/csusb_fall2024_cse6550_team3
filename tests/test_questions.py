import os
import json
import time 
import pytest
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path

CORPUS_SOURCE = Path("/app/data/swebok")
os.environ["CORPUS_SOURCE"] = str(CORPUS_SOURCE)

from backend.inference import chat_completion

class TestQuestionAnswers:
    """Test suite for Textbook Chatbot."""
    
    NO_CONTEXT_MSG = """
        I'm a chatbot that answers questions about SWEBOK (Software Engineering Body of Knowledge).
        Your question appears to be about something else.
        Could you ask a question related to software engineering fundamentals, requirements, design, construction, testing, maintenance, configuration management, engineering management, processes, models, or quality?
    """
    
    @staticmethod
    def load_test_questions(file_path: Path) -> Dict:
        """Load test questions from JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_results(results: List[Dict]) -> None:
        """Save test results to JSON file in tests/test_outputs/."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        # Create path to tests/test_outputs/
        output_dir = Path(__file__).parent / 'test_outputs'
        output_path = output_dir / filename
        
        # Create directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)

    @pytest.fixture
    def test_data(self) -> Dict:
        """Fixture to load test questions."""
        questions_path = Path(__file__).parent / 'questions.json'
        return self.load_test_questions(questions_path)

    def get_chat_response(self, question: str) -> Tuple[str, str]:
        """Helper method to get response from chat completion."""
        try:
            time.sleep(1)
            return next(chat_completion(question))
        except Exception as e:
            pytest.fail(f"Chat completion failed for question '{question}': {str(e)}")

    @pytest.mark.parametrize("question_set", [0])
    def test_answerable_questions(self, test_data: Dict, question_set: int):
        """Test that answerable questions get appropriate responses."""
        results = []
        
        for question in test_data['questions'][question_set]['answerable']:
            if not question:
                continue
                
            response, model_name = self.get_chat_response(question)
            
            result = {
                'question': question,
                'response': response,
                'type': 'answerable',
                'passed': self.NO_CONTEXT_MSG not in response
            }
            results.append(result)
            
            assert self.NO_CONTEXT_MSG not in response, \
                f"Question '{question}' incorrectly triggered no-context message"

        self.save_results(results)

    @pytest.mark.parametrize("question_set", [0])
    def test_unanswerable_questions(self, test_data: Dict, question_set: int):
        """Test that unanswerable questions get no-context responses."""
        results = []

        for question in test_data['questions'][question_set]['unanswerable']:
            if not question:
                continue

            response, model_name = self.get_chat_response(question)
            has_no_context = self.NO_CONTEXT_MSG.strip() in response.strip()

            result = {
                'question': question,
                'response': response,
                'type': 'unanswerable',
                'passed': has_no_context
            }
            results.append(result)

            assert has_no_context, \
                f"Question '{question}' should have triggered no-context message"

        self.save_results(results)

    def test_empty_question_sets(self, test_data: Dict):
        """Test handling of empty question sets."""
        empty_set = test_data['questions'][1]
        assert len(empty_set['answerable']) == 0
        assert len(empty_set['unanswerable']) == 0