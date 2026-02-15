"""
Ranking Engine - Main interface for candidate ranking
"""

from .candidate_scorer import CandidateScorer
from .job_matcher import JobMatcher

class RankingEngine:
    def __init__(self):
        self.scorer = CandidateScorer()
        self.matcher = JobMatcher()
    
    def rank_candidates(self, candidates, job_requirements):
        """Rank candidates based on job requirements"""
        ranked = []
        
        for candidate in candidates:
            # Score candidate
            score_result = self.scorer.score_candidate(candidate, job_requirements)
            
            # Combine with candidate data
            ranked.append({
                'candidate_id': candidate.get('file_path', 'unknown'),
                'name': candidate.get('entities', {}).get('name'),
                'email': candidate.get('entities', {}).get('email'),
                'total_score': score_result['total_score'],
                'grade': score_result['grade'],
                'breakdown': score_result['breakdown'],
                'skills': self._get_skills_summary(candidate),
                'candidate_data': candidate
            })
        
        # Sort by score
        ranked.sort(key=lambda x: x['total_score'], reverse=True)
        
        return ranked
    
    def match_to_job(self, candidates, job_description, job_requirements):
        """Match and rank candidates for a specific job"""
        # First, match by similarity
        matched = self.matcher.match_candidates(candidates, job_description)
        
        # Then score each
        results = []
        for item in matched:
            candidate = item['candidate']
            score_result = self.scorer.score_candidate(candidate, job_requirements)
            
            # Combined score: 50% similarity + 50% requirements match
            combined_score = (item['similarity_score'] * 0.5) + (score_result['total_score'] * 0.5)
            
            results.append({
                'candidate_id': candidate.get('file_path', 'unknown'),
                'name': candidate.get('entities', {}).get('name'),
                'email': candidate.get('entities', {}).get('email'),
                'combined_score': round(combined_score, 2),
                'similarity_score': item['similarity_score'],
                'requirements_score': score_result['total_score'],
                'grade': score_result['grade'],
                'skills': self._get_skills_summary(candidate)
            })
        
        return results
    
    def _get_skills_summary(self, candidate):
        """Get summary of candidate skills"""
        skills = []
        for cat, skill_list in candidate.get('skills', {}).get('technical', {}).items():
            skills.extend(skill_list)
        return skills[:10]  # Top 10 skills
