"""
Job Matcher - Match candidates to job requirements
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
    
    def match_candidates(self, candidates, job_description):
        """Match candidates to job description"""
        if not candidates:
            return []
        
        # Prepare texts
        job_text = job_description.lower()
        candidate_texts = [self._prepare_candidate_text(c) for c in candidates]
        
        # Calculate similarity
        all_texts = [job_text] + candidate_texts
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Add similarity scores to candidates
            results = []
            for i, candidate in enumerate(candidates):
                results.append({
                    'candidate': candidate,
                    'similarity_score': round(float(similarities[i]) * 100, 2)
                })
            
            # Sort by similarity
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results
        
        except:
            # Fallback: simple keyword matching
            return self._simple_match(candidates, job_text)
    
    def _prepare_candidate_text(self, candidate):
        """Prepare candidate text for matching"""
        text = candidate.get('raw_text', '')
        
        # Add skills
        skills = []
        for cat, skill_list in candidate.get('skills', {}).get('technical', {}).items():
            skills.extend(skill_list)
        
        return text + ' ' + ' '.join(skills)
    
    def _simple_match(self, candidates, job_text):
        """Simple keyword-based matching"""
        job_words = set(job_text.split())
        
        results = []
        for candidate in candidates:
            candidate_text = self._prepare_candidate_text(candidate).lower()
            candidate_words = set(candidate_text.split())
            
            # Calculate overlap
            overlap = len(job_words.intersection(candidate_words))
            score = (overlap / len(job_words)) * 100 if job_words else 0
            
            results.append({
                'candidate': candidate,
                'similarity_score': round(score, 2)
            })
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results
