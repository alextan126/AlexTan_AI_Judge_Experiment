import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAS_API_URL = "http://localhost:8000/api/v1/agent/exam"

CALLBACK_HOST = "localhost"
CALLBACK_PORT = 9876

SAMPLES_DIR = os.path.join(PROJECT_ROOT, "Samples")
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

TEST_ROUNDS = 5

CALLBACK_TIMEOUT_SECONDS = 600

QUESTION_TYPES = ["concept", "application", "code"]

DECISION_POINTS_MAP = {
    "concept": ["define"],
    "application": ["correct_option"],
    "code": ["syntax_correct", "function_correct", "asr_match"],
}

EXTRA_POINTS_MAP = {
    "concept": [
        "keyword", "keyword_first_sentence", "keyword_no_repeat",
        "not_overtime", "define_first_sentence", "order_define_explain",
    ],
    "application": ["hook_question", "derivation_correct"],
    "code": [
        "time_optimal", "space_optimal", "code_readability", "comment_readability",
    ],
}
