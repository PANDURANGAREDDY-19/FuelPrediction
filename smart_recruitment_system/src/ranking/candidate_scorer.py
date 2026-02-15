"""
Candidate Scorer - Score candidates based on resume and requirements
"""

class CandidateScorer:
    def __init__(self):
        self.weights = {
            'skills_match': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'profile_completeness': 0.1
        }
    
    def score_candidate(self, candidate_data, job_requirements):
        """Calculate overall candidate score"""
        scores = {
            'skills_match': self._score_skills(candidate_data, job_requirements),
            'experience': self._score_experience(candidate_data),
            'education': self._score_education(candidate_data),
            'profile_completeness': self._score_completeness(candidate_data)
        }
        
        # Weighted total
        total_score = sum(scores[k] * self.weights[k] for k in scores)
        
        return {
            'total_score': round(total_score, 2),
            'breakdown': scores,
            'grade': self._get_grade(total_score)
        }
    
    def _score_skills(self, candidate_data, job_requirements):
        """Score based on skill match"""
        candidate_skills = set()
        for cat, skills in candidate_data.get('skills', {}).get('technical', {}).items():
            candidate_skills.update(skills)
        
        required_skills = set(job_requirements.get('required_skills', []))
        
        if not required_skills:
            return 50.0
        
        matched = candidate_skills.intersection(required_skills)
        score = (len(matched) / len(required_skills)) * 100
        
        return min(score, 100.0)
    
    def _score_experience(self, candidate_data):
        """Score based on experience indicators"""
        text = candidate_data.get('raw_text', '').lower()
        
        # Simple heuristic: look for experience keywords
        exp_keywords = ['years', 'experience', 'worked', 'developed', 'led', 'managed']
        score = sum(10 for kw in exp_keywords if kw in text)
        
        return min(score, 100.0)
    
    def _score_education(self, candidate_data):
        """Score based on education"""
        text = candidate_data.get('raw_text', '').lower()
        
        edu_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        score = sum(15 for kw in edu_keywords if kw in text)
        
        return min(score, 100.0)
    
    def _score_completeness(self, candidate_data):
        """Score profile completeness"""
        entities = candidate_data.get('entities', {})
        
        score = 0
        if entities.get('email'): score += 25
        if entities.get('phone'): score += 25
        if entities.get('linkedin'): score += 25
        if entities.get('github'): score += 25
        
        return score
    
    def _get_grade(self, score):
        """Convert score to grade"""
        if score >= 80: return 'A'
        if score >= 60: return 'B'
        if score >= 40: return 'C'
        return 'D'
