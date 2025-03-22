from collections import defaultdict
from typing import Dict, List, Any, Tuple
import re
from . import EmailProcessor, EmailData  


class EmailClassifier(EmailProcessor):
    name = "classifier"
    description = "Classifies emails into predefined categories based on keywords, with confidence scoring."

    CATEGORIES = {
        "Application confirmation": ["thank you for applying", "application received", "we have received your application"],
        "OA invitation": ["online assessment", "coding test", "HackerRank", "CodeSignal", "assessment link"],
        "Interview request": ["interview", "schedule a call", "speak with you", "chat about your application"],
        "Rejection": ["unfortunately", "we regret to inform you", "not moving forward", "consider other candidates"],
        "Offer": ["excited to offer", "we are pleased to offer", "congratulations", "job offer"],
        "Other": []
    }

    CONFIDENCE_THRESHOLD = 0.05 

    def classify_email(self, email: EmailData) -> Tuple[str, float, List[str]]:
        """Classify an email and return category, confidence score, and matched keywords."""
        scores = defaultdict(int)
        matched_keywords = []
        content = f"{email.subject} {email.content}".lower()

        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if re.search(rf"\b{re.escape(keyword)}\b", content):
                    scores[category] += 1
                    matched_keywords.append(keyword)  

        if scores:
            max_score = max(scores.values())
            top_categories = [cat for cat, score in scores.items() if score == max_score]
            
            if len(top_categories) == 1:
                category = top_categories[0]
                sorted_scores = sorted(scores.values(), reverse=True)
                s1 = sorted_scores[0]
                s2 = sorted_scores[1] if len(sorted_scores) > 1 else 0
                confidence = abs(s1 - s2) / s1 if s1 else 0.0
            else:
                # Option 1: Send to human review
                # category = "Human Review Needed"
                # confidence = 0.0
                
                # Option 2: Use a priority-based tiebreaker
                priorities = {"offer": 2, "interview request": 2,"thank you for applying":1}
                category = max(top_categories, key=lambda x: priorities.get(x, 0))
                confidence = 0.5  
                                
            return category, confidence, matched_keywords
        return "Other", 1.0, []


    def process(self, emails: List[EmailData]) -> Dict[str, Any]:
        """Process a list of emails and classify them with confidence scores and matched keywords."""
        results = {}

        for email in emails:
            category, confidence, matched_keywords = self.classify_email(email)
            
            results[email.subject] = {
                "category": category,
                "confidence": confidence,
                "matched_keywords": matched_keywords
            }

        return results

