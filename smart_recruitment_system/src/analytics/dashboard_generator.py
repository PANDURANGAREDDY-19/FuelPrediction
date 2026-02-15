"""
Dashboard Generator - Main interface for analytics dashboard
"""

from .analytics_generator import AnalyticsGenerator
from .visualization_generator import VisualizationGenerator
import json
from pathlib import Path

class DashboardGenerator:
    def __init__(self):
        self.analytics_gen = AnalyticsGenerator()
        self.viz_gen = VisualizationGenerator()
    
    def generate_dashboard(self, candidates):
        """Generate complete dashboard with analytics and visualizations"""
        # Generate analytics
        analytics = self.analytics_gen.generate_analytics(candidates)
        
        # Generate visualizations
        charts = self.viz_gen.generate_all_charts(analytics)
        
        # Save analytics
        output_path = Path('data/processed/dashboard_analytics.json')
        with open(output_path, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        return {
            'analytics': analytics,
            'charts': charts,
            'analytics_file': str(output_path)
        }
    
    def print_summary(self, analytics):
        """Print analytics summary"""
        print("\n" + "="*60)
        print("  📊 HIRING ANALYTICS DASHBOARD")
        print("="*60 + "\n")
        
        # Overview
        overview = analytics['overview']
        print("📈 Overview:")
        print(f"  Total Candidates: {overview['total_candidates']}")
        print(f"  Average Score: {overview['avg_score']:.1f}")
        print(f"  Score Range: {overview['min_score']:.1f} - {overview['max_score']:.1f}")
        print(f"  With Email: {overview['candidates_with_email']}")
        print(f"  With LinkedIn: {overview['candidates_with_linkedin']}")
        
        # Skills
        skills = analytics['skills_distribution']
        print(f"\n💻 Skills:")
        print(f"  Unique Skills: {skills['total_unique_skills']}")
        if skills['top_skills']:
            top_3 = list(skills['top_skills'].items())[:3]
            print(f"  Top 3: {', '.join([f'{k}({v})' for k, v in top_3])}")
        
        # Grades
        grades = analytics['score_distribution']['grade_distribution']
        print(f"\n🎓 Grade Distribution:")
        for grade, count in sorted(grades.items()):
            print(f"  Grade {grade}: {count} candidates")
        
        # Top Candidates
        top = analytics['top_candidates']
        if top:
            print(f"\n🏆 Top 3 Candidates:")
            for i, candidate in enumerate(top[:3], 1):
                print(f"  {i}. {candidate['name']} - Score: {candidate['score']:.1f} (Grade {candidate['grade']})")
