"""
Job Description Matcher Module
Performs keyword-based matching between resume and JD to assess candidate fit.
"""

import re
from typing import Dict, List, Tuple


class JDMatcher:
    """
    Matches candidate resumes against job description using keyword analysis.
    Provides a simple fit score and classification.
    """

    def __init__(self, jd_file_path: str):
        """
        Initialize the JD matcher with a job description file.

        Args:
            jd_file_path: Path to the job description text file
        """
        self.jd_text = self.load_jd(jd_file_path)
        self.jd_keywords = self.extract_keywords(self.jd_text)

    def load_jd(self, file_path: str) -> str:
        """
        Load job description from a text file.

        Args:
            file_path: Path to JD text file

        Returns:
            JD text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                jd_text = file.read()
            print(f"[OK] Loaded JD from: {file_path}")
            return jd_text
        except Exception as e:
            print(f"[ERROR] Error loading JD file: {str(e)}")
            return ""

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.
        Focuses on technical skills, tools, and qualifications.

        Args:
            text: Text to extract keywords from

        Returns:
            List of keywords (lowercase, unique)
        """
        # Convert to lowercase for matching
        text_lower = text.lower()

        # Common technical keywords and skills patterns
        # You can extend this list based on your domain
        common_skills = [
            # Programming languages
            'python', 'java', 'javascript', 'c\\+\\+', 'c#', 'ruby', 'php', 'go', 'rust',
            'swift', 'kotlin', 'typescript', 'scala', 'r programming',

            # Web frameworks
            'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'node.js', 'express',
            'spring', 'asp.net', 'laravel', 'rails',

            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'cassandra',
            'dynamodb', 'elasticsearch',

            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
            'ansible', 'ci/cd', 'devops', 'linux',

            # Data Science & ML
            'machine learning', 'deep learning', 'data science', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'jupyter',

            # Other technical
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'git',
            'testing', 'unit testing', 'integration testing',

            # Soft skills
            'communication', 'leadership', 'team player', 'problem solving',
            'analytical', 'collaboration'
        ]

        # Find all skill keywords present in the text
        found_keywords = []
        for skill in common_skills:
            # Use word boundary for better matching
            pattern = r'\b' + skill + r'\b'
            if re.search(pattern, text_lower):
                # Clean up the keyword (remove regex characters)
                clean_skill = skill.replace('\\+\\+', '++').replace('\\', '')
                found_keywords.append(clean_skill)

        # Also extract years of experience mentioned
        experience_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        exp_matches = re.findall(experience_pattern, text_lower)
        if exp_matches:
            found_keywords.append(f"{exp_matches[0]}+ years experience")

        # Remove duplicates while preserving order
        unique_keywords = list(dict.fromkeys(found_keywords))

        print(f"[OK] Extracted {len(unique_keywords)} keywords from JD")
        return unique_keywords

    def calculate_match_score(self, resume_text: str) -> Tuple[int, List[str], List[str]]:
        """
        Calculate how well a resume matches the JD based on keyword overlap.

        Args:
            resume_text: Full text of the candidate's resume

        Returns:
            Tuple of (match_score, matched_keywords, missing_keywords)
        """
        resume_lower = resume_text.lower()

        matched_keywords = []
        missing_keywords = []

        # Check each JD keyword against the resume
        for keyword in self.jd_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, resume_lower):
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)

        # Calculate percentage match
        if len(self.jd_keywords) > 0:
            match_score = int((len(matched_keywords) / len(self.jd_keywords)) * 100)
        else:
            match_score = 0

        return match_score, matched_keywords, missing_keywords

    def get_fit_label(self, score: int) -> str:
        """
        Convert numerical score to a fit label.

        Args:
            score: Match score (0-100)

        Returns:
            Fit label (Strong Fit, Good Fit, Moderate Fit, Weak Fit)
        """
        if score >= 70:
            return "Strong Fit"
        elif score >= 50:
            return "Good Fit"
        elif score >= 30:
            return "Moderate Fit"
        else:
            return "Weak Fit"

    def generate_screening_comment(self, score: int, matched: List[str], missing: List[str]) -> str:
        """
        Generate a human-readable screening comment.

        Args:
            score: Match score
            matched: List of matched keywords
            missing: List of missing keywords

        Returns:
            Screening comment string
        """
        comment_parts = []

        # Add score summary
        comment_parts.append(f"Match Score: {score}%.")

        # Add matched skills (top 5)
        if matched:
            top_matched = matched[:5]
            comment_parts.append(f"Key skills: {', '.join(top_matched)}.")

        # Add missing critical skills (top 3)
        if missing and score < 70:
            top_missing = missing[:3]
            comment_parts.append(f"Missing: {', '.join(top_missing)}.")

        return " ".join(comment_parts)

    def evaluate_candidate(self, candidate_info: Dict) -> Dict:
        """
        Evaluate a candidate against the JD and add fit assessment.

        Args:
            candidate_info: Dictionary containing candidate information including resume_text

        Returns:
            Updated candidate_info with fit score and labels
        """
        resume_text = candidate_info.get('resume_text', '')

        if not resume_text:
            print("[ERROR] No resume text available for matching")
            candidate_info['auto_fit_score'] = 0
            candidate_info['auto_fit_label'] = "Cannot Evaluate"
            candidate_info['auto_screen_comment'] = "No resume text found"
            return candidate_info

        # Calculate match
        score, matched, missing = self.calculate_match_score(resume_text)

        # Get fit label
        fit_label = self.get_fit_label(score)

        # Generate comment
        comment = self.generate_screening_comment(score, matched, missing)

        # Update candidate info
        candidate_info['auto_fit_score'] = score
        candidate_info['auto_fit_label'] = fit_label
        candidate_info['auto_screen_comment'] = comment

        print(f"[OK] Evaluated {candidate_info['candidate_name']}: {score}% ({fit_label})")

        # Remove resume_text before returning (no need to store in sheet)
        if 'resume_text' in candidate_info:
            del candidate_info['resume_text']

        return candidate_info

    def evaluate_multiple_candidates(self, candidates_list: List[Dict]) -> List[Dict]:
        """
        Evaluate multiple candidates against the JD.

        Args:
            candidates_list: List of candidate dictionaries

        Returns:
            List of evaluated candidates with fit scores
        """
        evaluated_candidates = []

        for candidate in candidates_list:
            evaluated = self.evaluate_candidate(candidate)
            evaluated_candidates.append(evaluated)

        return evaluated_candidates


# Example usage (for testing)
if __name__ == "__main__":
    # Initialize matcher with a JD file
    matcher = JDMatcher("../jd_files/python_developer_jd.txt")

    # Print extracted keywords
    print("\nExtracted JD Keywords:")
    for i, keyword in enumerate(matcher.jd_keywords, 1):
        print(f"{i}. {keyword}")

    # Test with sample resume text
    sample_resume = """
    John Doe
    john@example.com | +1-234-567-8900

    Senior Python Developer with 5 years of experience.

    Skills: Python, Django, Flask, PostgreSQL, AWS, Docker, Git
    Experience with REST APIs and microservices architecture.
    Strong problem-solving and communication skills.
    """

    test_candidate = {
        'candidate_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1-234-567-8900',
        'location': 'New York',
        'resume_text': sample_resume
    }

    # Evaluate candidate
    evaluated = matcher.evaluate_candidate(test_candidate)

    print("\n--- Evaluation Results ---")
    print(f"Score: {evaluated['auto_fit_score']}")
    print(f"Label: {evaluated['auto_fit_label']}")
    print(f"Comment: {evaluated['auto_screen_comment']}")
