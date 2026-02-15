"""
Resume NLP Engine - Main interface for resume processing
"""

from .resume_parser import ResumeParser
from .entity_recognizer import EntityRecognizer
from .skill_extractor import SkillExtractor
from .text_preprocessor import TextPreprocessor

class ResumeNLPEngine:
    def __init__(self):
        self.parser = ResumeParser()
        self.entity_recognizer = EntityRecognizer()
        self.skill_extractor = SkillExtractor()
        self.preprocessor = TextPreprocessor()
    
    def process_resume(self, file_path):
        """Complete resume processing pipeline"""
        # Parse resume
        text = self.parser.parse(file_path)
        
        # Extract entities
        entities = self.entity_recognizer.extract_entities(text)
        
        # Extract skills
        skills = self.skill_extractor.extract_skills(text)
        
        # Extract sections
        sections = self.preprocessor.extract_sections(text)
        
        return {
            'file_path': str(file_path),
            'raw_text': text,
            'entities': entities,
            'skills': skills,
            'sections': sections,
            'summary': self._generate_summary(entities, skills)
        }
    
    def _generate_summary(self, entities, skills):
        """Generate candidate summary"""
        tech_skills = []
        for category, skill_list in skills.get('technical', {}).items():
            tech_skills.extend(skill_list)
        
        return {
            'name': entities.get('name'),
            'email': entities.get('email'),
            'phone': entities.get('phone'),
            'total_technical_skills': len(tech_skills),
            'total_soft_skills': len(skills.get('soft', [])),
            'has_linkedin': entities.get('linkedin') is not None,
            'has_github': entities.get('github') is not None
        }
