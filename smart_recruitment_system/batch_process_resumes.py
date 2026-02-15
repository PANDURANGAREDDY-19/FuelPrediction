"""
Batch Resume Processor - Process all resumes in subdirectories
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.nlp_engine import ResumeNLPEngine

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def process_all_resumes():
    print_header("📄 BATCH RESUME PROCESSING")
    
    # Find all PDF files recursively
    resume_dir = Path("data/resumes")
    resumes = list(resume_dir.rglob("*.pdf")) + list(resume_dir.rglob("*.docx"))
    
    if not resumes:
        print("⚠️  No resumes found")
        return
    
    print(f"Found {len(resumes)} resume(s)")
    print(f"Processing first 5 resumes...\n")
    
    # Initialize engine
    engine = ResumeNLPEngine()
    
    # Process first 5 resumes
    results = []
    for i, resume_path in enumerate(resumes[:5], 1):
        print(f"\n[{i}/5] Processing: {resume_path.name}")
        
        try:
            result = engine.process_resume(resume_path)
            
            # Print summary
            entities = result['entities']
            skills = result['skills']
            
            print(f"  Name: {entities.get('name') or 'Not found'}")
            print(f"  Email: {entities.get('email') or 'Not found'}")
            
            tech_skills = []
            for cat, skill_list in skills.get('technical', {}).items():
                tech_skills.extend(skill_list)
            
            print(f"  Technical Skills: {len(tech_skills)}")
            if tech_skills:
                print(f"    {', '.join(tech_skills[:5])}")
            
            results.append(result)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Save results
    output_path = Path("data/processed/batch_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print_header("✅ BATCH PROCESSING COMPLETE")
    print(f"\nProcessed: {len(results)} resumes")
    print(f"Saved to: {output_path}")
    print(f"\nTotal resumes available: {len(resumes)}")

if __name__ == "__main__":
    try:
        process_all_resumes()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
