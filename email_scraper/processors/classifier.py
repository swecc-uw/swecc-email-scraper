import re
from collections import defaultdict
from typing import Any, ClassVar, Dict, List

from . import EmailData, EmailProcessor


class EmailClassifier(EmailProcessor):
    name = "classifier"
    description = "Classifies emails into categories based on keywords."

    CATEGORIES: ClassVar[Dict[str, List[str]]] = {
        "Application confirmation": [
            "thank you for applying",
            "application received",
            "we have received your application",
            "thank you so much for taking the time to apply",
        ],
        "OA invitation": [
            "online assessment",
            "coding test",
            "hackerrank",
            "codeSignal",
            "assessment link",
        ],
        "Interview request": [
            "interview",
            "schedule a call",
            "speak with you",
            "chat about your application",
        ],
        "Rejection": [
            "unfortunately",
            "we regret to inform you",
            "not moving forward",
            "consider other candidates",
            "decided not to move forward with your application",
        ],
        "Offer": [
            "excited to offer",
            "we are pleased to offer",
            "congratulations",
            "job offer",
        ],
        "Other": [],
    }

    CONFIDENCE_THRESHOLD: ClassVar[float] = 0.05

    def classify_email(self, email: EmailData) -> Dict[str, Any]:
        """Classify an email and return category, confidence score, and matched keywords."""
        scores = defaultdict(int)
        matched_keywords = []

        try:
            content = f"{email.subject} {email.content}"
            for category, keywords in self.CATEGORIES.items():
                for keyword in keywords:
                    pattern = rf"{re.escape(keyword)}"
                    if re.search(pattern, content, re.IGNORECASE):
                        scores[category] += 1
                        matched_keywords.append(keyword)

            if scores:
                # Find the maximum score and corresponding categories
                max_score = max(scores.values())
                top_categories = [
                    cat for cat, score in scores.items() if score == max_score
                ]

                if len(top_categories) == 1:
                    category = top_categories[0]
                    sorted_scores = sorted(scores.values(), reverse=True)
                    s1 = sorted_scores[0]
                    s2 = sorted_scores[1] if len(sorted_scores) > 1 else 0
                    confidence = abs(s1 - s2) / s1 if s1 else 0.0
                else:
                    category = "Human Review Needed"
                    confidence = 0.5
            else:
                category = "Other"
                confidence = 1.0

        except Exception as e:
            category = "Processing Error"
            confidence = 0.0
            matched_keywords = [f"Error: {e!s}"]
            return category, confidence, matched_keywords

        return category, confidence, matched_keywords

    def process(self, emails: List[EmailData]) -> Dict[str, Any]:
        """Process a list of emails and classify them with
        confidence scores and matched keywords."""
        classifications = []

        for email in emails:
            category, confidence, matched_keywords = self.classify_email(email)

            classifications.append(
                {
                    "subject": email.subject,
                    "category": category,
                    "confidence": confidence,
                    "matched_keywords": matched_keywords,
                }
            )

        return {"classifications": classifications}
