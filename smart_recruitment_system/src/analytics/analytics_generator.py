"""
Analytics Generator - Generate hiring analytics and insights
"""

import json
from collections import Counter
from pathlib import Path

class AnalyticsGenerator:
    def __init__(self):
        pass
    
    def generate_analytics(self, candidates):
        """Generate comprehensive analytics from candidates"""
        if not candidates:
            return self._empty_analytics()
        
        return {
            'overview': self._generate_overview(candidates),
            'skills_distribution': self._analyze_skills(candidates),
            'score_distribution': self._analyze_scores(candidates),
            'profile_completeness': self._analyze_completeness(candidates),
            'top_candidates': self._get_top_candidates(candidates, 5)
        }
    
    def _generate_overview(self, candidates):
        """Generate overview statistics"""
        scores = [c.get('total_score', 0) for c in candidates if 'total_score' in c]
        
        return {
            'total_candidates': len(candidates),
            'avg_score': round(sum(scores) / len(scores), 2) if scores else 0,
            'max_score': max(scores) if scores else 0,
            'min_score': min(scores) if scores else 0,
            'candidates_with_email': sum(1 for c in candidates if c.get('candidate_data', {}).get('entities', {}).get('email')),
            'candidates_with_linkedin': sum(1 for c in candidates if c.get('candidate_data', {}).get('entities', {}).get('linkedin'))
        }
    
    def _analyze_skills(self, candidates):
        """Analyze skill distribution"""
        all_skills = []
        
        for candidate in candidates:
            skills_data = candidate.get('candidate_data', {}).get('skills', {})
            for category, skill_list in skills_data.get('technical', {}).items():
                all_skills.extend(skill_list)
        
        skill_counts = Counter(all_skills)
        
        return {
            'total_unique_skills': len(skill_counts),
            'top_skills': dict(skill_counts.most_common(10)),
            'skill_categories': self._count_skill_categories(candidates)
        }
    
    def _analyze_scores(self, candidates):
        """Analyze score distribution"""
        grades = [c.get('grade', 'D') for c in candidates]
        grade_counts = Counter(grades)
        
        return {
            'grade_distribution': dict(grade_counts),
            'a_grade_count': grade_counts.get('A', 0),
            'b_grade_count': grade_counts.get('B', 0),
            'c_grade_count': grade_counts.get('C', 0),
            'd_grade_count': grade_counts.get('D', 0)
        }
    
    def _analyze_completeness(self, candidates):
        """Analyze profile completeness"""
        complete_profiles = 0
        
        for candidate in candidates:
            entities = candidate.get('candidate_data', {}).get('entities', {})
            if entities.get('email') and entities.get('phone'):
                complete_profiles += 1
        
        return {
            'complete_profiles': complete_profiles,
            'incomplete_profiles': len(candidates) - complete_profiles,
            'completeness_rate': round((complete_profiles / len(candidates)) * 100, 2) if candidates else 0
        }
    
    def _get_top_candidates(self, candidates, n=5):
        """Get top N candidates"""
        sorted_candidates = sorted(candidates, key=lambda x: x.get('total_score', 0), reverse=True)
        
        return [{
            'name': c.get('name') or 'Unknown',
            'score': c.get('total_score', 0),
            'grade': c.get('grade', 'D'),
            'email': c.get('email')
        } for c in sorted_candidates[:n]]
    
    def _count_skill_categories(self, candidates):
        """Count skills by category"""
        categories = Counter()
        
        for candidate in candidates:
            skills_data = candidate.get('candidate_data', {}).get('skills', {})
            for category in skills_data.get('technical', {}).keys():
                categories[category] += 1
        
        return dict(categories)
    
    def _empty_analytics(self):
        """Return empty analytics structure"""
        return {
            'overview': {'total_candidates': 0, 'avg_score': 0},
            'skills_distribution': {'total_unique_skills': 0, 'top_skills': {}},
            'score_distribution': {'grade_distribution': {}},
            'profile_completeness': {'complete_profiles': 0},
            'top_candidates': []
        }
