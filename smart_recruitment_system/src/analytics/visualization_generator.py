"""
Visualization Generator - Create charts and visualizations
"""

import matplotlib.pyplot as plt
from pathlib import Path

class VisualizationGenerator:
    def __init__(self, output_dir='data/visualizations'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_charts(self, analytics):
        """Generate all visualization charts"""
        charts = []
        
        # Skills distribution
        if analytics['skills_distribution']['top_skills']:
            charts.append(self.create_skills_chart(analytics['skills_distribution']))
        
        # Score distribution
        if analytics['score_distribution']['grade_distribution']:
            charts.append(self.create_grade_chart(analytics['score_distribution']))
        
        # Profile completeness
        charts.append(self.create_completeness_chart(analytics['profile_completeness']))
        
        return charts
    
    def create_skills_chart(self, skills_data):
        """Create skills distribution bar chart"""
        top_skills = skills_data['top_skills']
        
        if not top_skills:
            return None
        
        plt.figure(figsize=(10, 6))
        skills = list(top_skills.keys())[:10]
        counts = list(top_skills.values())[:10]
        
        plt.barh(skills, counts, color='skyblue')
        plt.xlabel('Number of Candidates')
        plt.title('Top 10 Skills Distribution')
        plt.tight_layout()
        
        output_path = self.output_dir / 'skills_distribution.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_grade_chart(self, score_data):
        """Create grade distribution pie chart"""
        grades = score_data['grade_distribution']
        
        if not grades:
            return None
        
        plt.figure(figsize=(8, 8))
        labels = list(grades.keys())
        sizes = list(grades.values())
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Candidate Grade Distribution')
        plt.axis('equal')
        
        output_path = self.output_dir / 'grade_distribution.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_completeness_chart(self, completeness_data):
        """Create profile completeness chart"""
        plt.figure(figsize=(8, 6))
        
        labels = ['Complete', 'Incomplete']
        sizes = [
            completeness_data['complete_profiles'],
            completeness_data['incomplete_profiles']
        ]
        colors = ['#2ecc71', '#e74c3c']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Profile Completeness')
        plt.axis('equal')
        
        output_path = self.output_dir / 'profile_completeness.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
