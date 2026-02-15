"""
Skill Extractor - Extract technical and soft skills from resume text
"""
import re

class SkillExtractor:
    def __init__(self):
        # Expanded technical skills database
        self.tech_skills = {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 
                'swift', 'kotlin', 'typescript', 'scala', 'r', 'matlab', 'perl'
            ],
            'web': [
                'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'django', 'flask', 
                'fastapi', 'express', 'nextjs', 'nuxt', 'svelte', 'bootstrap', 'tailwind'
            ],
            'database': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 
                'dynamodb', 'cassandra', 'elasticsearch', 'mariadb'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 
                'ansible', 'cloudformation', 'lambda', 'ec2', 's3'
            ],
            'ml_ai': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 
                'scikit-learn', 'nlp', 'computer vision', 'opencv', 'pandas', 'numpy'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'vscode', 
                'jupyter', 'postman', 'swagger', 'linux', 'bash'
            ]
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'critical thinking', 'time management', 'adaptability', 'creativity',
            'collaboration', 'presentation', 'negotiation', 'project management'
        ]
    
    def extract_skills(self, text):
        """Extract all skills from resume text"""
        text_lower = text.lower()
        
        found_skills = {
            'technical': {},
            'soft': []
        }
        
        # Extract technical skills by category
        for category, skills in self.tech_skills.items():
            found = []
            for skill in skills:
                # Use word boundary for accurate matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(skill.title())
            
            if found:
                found_skills['technical'][category] = sorted(set(found))
        
        # Extract soft skills
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills['soft'].append(skill.title())
        
        found_skills['soft'] = sorted(set(found_skills['soft']))
        
        return found_skills
    
    def get_all_technical_skills(self, skills_dict):
        """Flatten technical skills into single list"""
        all_skills = []
        for category, skills in skills_dict.get('technical', {}).items():
            all_skills.extend(skills)
        return sorted(set(all_skills))
    
    def count_skills(self, skills_dict):
        """Count total skills"""
        tech_count = sum(len(v) for v in skills_dict.get('technical', {}).values())
        soft_count = len(skills_dict.get('soft', []))
        return {'technical': tech_count, 'soft': soft_count, 'total': tech_count + soft_count}
