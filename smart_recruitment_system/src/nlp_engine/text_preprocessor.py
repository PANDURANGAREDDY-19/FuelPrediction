"""
Text Preprocessor - Clean and normalize resume text
"""

import re

class TextPreprocessor:
    def __init__(self):
        self.stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    
    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        text = self.lowercase(text)
        text = self.remove_urls(text)
        text = self.remove_extra_spaces(text)
        return text
    
    def lowercase(self, text):
        """Convert to lowercase"""
        return text.lower()
    
    def remove_urls(self, text):
        """Remove URLs"""
        return re.sub(r'http\S+|www\.\S+', '', text)
    
    def remove_extra_spaces(self, text):
        """Remove extra whitespace"""
        return re.sub(r'\s+', ' ', text).strip()
    
    def extract_sections(self, text):
        """Extract resume sections"""
        sections = {}
        
        # Common section headers
        patterns = {
            'education': r'education|academic|qualification',
            'experience': r'experience|employment|work history',
            'skills': r'skills|technical skills|competencies',
            'projects': r'projects|portfolio',
            'certifications': r'certifications|certificates|licenses'
        }
        
        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sections[section] = match.start()
        
        return sections
