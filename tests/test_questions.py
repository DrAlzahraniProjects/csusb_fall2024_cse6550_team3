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
    
    NO_CONTEXT_MSG = "<p>I'm a chatbot that only answers questions about <a href=\"https://www.computer.org/education/bodies-of-knowledge/software-engineering\">SWEBOK (Software Engineering Body of Knowledge).</a><br> Your question appears to be about something else. Could you ask a question related to SWEBOK?</p>"
    
    @staticmethod
    def load_test_questions(file_path: Path) -> Dict:
        """Load test questions from JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_results(results: Dict) -> None:
        """Save test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        output_dir = Path(__file__).parent / 'test_outputs'
        output_path = output_dir / filename
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)

    @pytest.fixture
    def test_data(self) -> Dict:
        """Load test questions."""
        questions_path = Path(__file__).parent / 'questions.json'
        return self.load_test_questions(questions_path)
        
    @pytest.fixture(scope="class")
    def test_results(self):
        """Class-level fixture to store results"""
        return {
            "answerable": {
                "test_type": "answerable",
                "summary": {"total_questions": 0, "correct_answers": 0, "incorrect_answers": 0, "accuracy": 0.0},
                "detailed_results": [],
                "failed_questions": []
            },
            "unanswerable": {
                "test_type": "unanswerable",
                "summary": {"total_questions": 0, "correct_answers": 0, "incorrect_answers": 0, "accuracy": 0.0},
                "detailed_results": [],
                "failed_questions": []
            }
        }

    def get_chat_response(self, question: str) -> str:
        """Helper method to get response from chat completion."""
        try:
            time.sleep(1)
            full_response = ""
            model_name = ""
            for chunk, model in chat_completion(question):
                full_response += chunk
                model_name = model
            return full_response, model_name
        except Exception as e:
            pytest.fail(f"Chat completion failed for question '{question}': {str(e)}")

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request, test_results):
        """Setup and teardown for tests"""
        yield
        
        # Only save results at the end of all tests
        if request.node.name == "test_unanswerable_questions":
            combined_results = {
                "timestamp": datetime.now().isoformat(),
                "answerable": test_results["answerable"],
                "unanswerable": test_results["unanswerable"],
                "overall_summary": {
                    "total_questions": test_results["answerable"]["summary"]["total_questions"] + 
                                     test_results["unanswerable"]["summary"]["total_questions"],
                    "total_correct": test_results["answerable"]["summary"]["correct_answers"] + 
                                   test_results["unanswerable"]["summary"]["correct_answers"],
                    "total_incorrect": test_results["answerable"]["summary"]["incorrect_answers"] + 
                                     test_results["unanswerable"]["summary"]["incorrect_answers"],
                    "overall_accuracy": (test_results["answerable"]["summary"]["correct_answers"] + 
                                       test_results["unanswerable"]["summary"]["correct_answers"]) / 
                                      (test_results["answerable"]["summary"]["total_questions"] + 
                                       test_results["unanswerable"]["summary"]["total_questions"]) * 100
                }
            }
            
            # Print consolidated summary
            print("\nTest Results Summary:")
            print(f"Total Questions Tested: {combined_results['overall_summary']['total_questions']}")
            print(f"Total Correct Answers: {combined_results['overall_summary']['total_correct']}")
            print(f"Total Incorrect Answers: {combined_results['overall_summary']['total_incorrect']}")
            print(f"Overall Accuracy: {combined_results['overall_summary']['overall_accuracy']:.2f}%")
            
            if test_results["answerable"]["failed_questions"] or test_results["unanswerable"]["failed_questions"]:
                print("\nFailed Questions:")
                for fail in test_results["answerable"]["failed_questions"]:
                    print(f"- {fail['question']} (Answerable)")
                for fail in test_results["unanswerable"]["failed_questions"]:
                    print(f"- {fail['question']} (Unanswerable)")
            
            self.save_results(combined_results)

    def test_answerable_questions(self, test_data: Dict, test_results):
        """Test that answerable questions are answered correctly"""
        total_questions = 0
        correct_answers = 0
        
        for question_set_idx in range(len(test_data['questions'])):
            for question in test_data['questions'][question_set_idx]['answerable']:
                if not question:
                    continue
                    
                total_questions += 1
                response, model_name = self.get_chat_response(question)
                is_correct = self.NO_CONTEXT_MSG not in response
                
                if is_correct:
                    correct_answers += 1
                else:
                    test_results["answerable"]["failed_questions"].append({
                        "question": question,
                        "expected": "Answer from knowledge base",
                        "received": "No context message"
                    })
                    
                result = {
                    'question': question,
                    'response': response,
                    'passed': is_correct,
                }
                test_results["answerable"]["detailed_results"].append(result)
        
        # Update summary statistics
        test_results["answerable"]["summary"]["total_questions"] = total_questions
        test_results["answerable"]["summary"]["correct_answers"] = correct_answers
        test_results["answerable"]["summary"]["incorrect_answers"] = total_questions - correct_answers
        test_results["answerable"]["summary"]["accuracy"] = correct_answers / total_questions if total_questions > 0 else 0
        
        assert correct_answers == total_questions, f"{total_questions - correct_answers} answerable questions failed"

    def test_unanswerable_questions(self, test_data: Dict, test_results):
        """Test that unanswerable questions are answered correctly"""
        total_questions = 0
        correct_answers = 0
        
        for question_set_idx in range(len(test_data['questions'])):
            for question in test_data['questions'][question_set_idx]['unanswerable']:
                if not question:
                    continue
                    
                total_questions += 1
                response, model_name = self.get_chat_response(question)
                is_correct = self.NO_CONTEXT_MSG in response
                
                if is_correct:
                    correct_answers += 1
                else:
                    test_results["unanswerable"]["failed_questions"].append({
                        "question": question,
                        "expected": "No context message",
                        "received": "Attempted answer"
                    })
                    
                result = {
                    'question': question,
                    'response': response,
                    'passed': is_correct,
                }
                test_results["unanswerable"]["detailed_results"].append(result)
        
        # Update summary statistics
        test_results["unanswerable"]["summary"]["total_questions"] = total_questions
        test_results["unanswerable"]["summary"]["correct_answers"] = correct_answers
        test_results["unanswerable"]["summary"]["incorrect_answers"] = total_questions - correct_answers
        test_results["unanswerable"]["summary"]["accuracy"] = correct_answers / total_questions if total_questions > 0 else 0
        
        assert correct_answers == total_questions, f"{total_questions - correct_answers} unanswerable questions failed"