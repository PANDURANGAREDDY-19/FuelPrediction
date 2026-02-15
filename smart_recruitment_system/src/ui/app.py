"""
Flask Web Application for Smart Recruitment System
"""
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import json
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.nlp_engine.resume_parser import ResumeParser
from src.ranking.ranking_engine import RankingEngine
from src.analytics.dashboard_generator import DashboardGenerator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components (lazy load face_detector to avoid deepface import)
face_detector = None
resume_parser = ResumeParser()
ranking_engine = RankingEngine()
dashboard_gen = DashboardGenerator()

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        
        # Save to uploads folder (temporary)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Parse resume using NLP engine
        from src.nlp_engine import ResumeNLPEngine
        nlp_engine = ResumeNLPEngine()
        result = nlp_engine.process_resume(upload_path)
        
        # Save to permanent storage for ranking
        permanent_folder = Path('data/resumes/uploaded')
        permanent_folder.mkdir(parents=True, exist_ok=True)
        permanent_path = permanent_folder / filename
        
        # Copy to permanent storage
        import shutil
        shutil.copy2(upload_path, permanent_path)
        
        # Save parsed data as JSON
        import json
        json_path = permanent_folder / f"{filename}.json"
        with open(json_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Extract data for response
        entities = result.get('entities', {})
        skills = result.get('skills', {})
        
        # Count total skills
        tech_count = sum(len(v) for v in skills.get('technical', {}).values())
        soft_count = len(skills.get('soft', []))
        total_skills = tech_count + soft_count
        
        return jsonify({
            'success': True,
            'filename': filename,
            'stored': True,
            'data': {
                'email': entities.get('email'),
                'phone': entities.get('phone'),
                'name': entities.get('name'),
                'linkedin': entities.get('linkedin'),
                'github': entities.get('github'),
                'skills': list(set(
                    [s for cat in skills.get('technical', {}).values() for s in cat] +
                    skills.get('soft', [])
                )),
                'total_skills': total_skills
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/verify_face', methods=['POST'])
def verify_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        from .simple_face_detector import OpenCVFaceDetector
        detector = OpenCVFaceDetector()
        faces = detector.detect_faces(filepath)
        
        return jsonify({
            'success': True,
            'faces_detected': len(faces),
            'faces': [{'confidence': float(f['confidence']), 'box': f['box']} for f in faces]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Face detection error: {str(e)}'
        }), 500

@app.route('/rank_candidates', methods=['POST'])
def rank_candidates():
    try:
        data = request.json
        job_desc = data.get('job_description', '')
        use_uploaded = data.get('use_uploaded', True)  # Use uploaded resumes by default
        
        if not job_desc.strip():
            return jsonify({
                'success': False,
                'error': 'Job description is required'
            }), 400
        
        # Process resumes from uploaded folder
        from src.nlp_engine import ResumeNLPEngine
        from pathlib import Path
        
        nlp_engine = ResumeNLPEngine()
        candidates = []
        
        # Check uploaded folder first
        uploaded_path = Path('data/resumes/uploaded')
        test_path = Path('data/resumes/test')
        
        # Use uploaded folder if it exists and has files
        if use_uploaded and uploaded_path.exists():
            resume_path = uploaded_path
        elif test_path.exists():
            resume_path = test_path
        else:
            return jsonify({
                'success': False,
                'error': 'No resume folders found'
            }), 404
        
        # Process all resumes in folder
        for file in resume_path.glob('*'):
            if file.suffix.lower() in ['.pdf', '.docx', '.txt']:
                try:
                    candidate_data = nlp_engine.process_resume(str(file))
                    candidates.append(candidate_data)
                except Exception:
                    continue
        
        if not candidates:
            return jsonify({
                'success': True,
                'candidates': [],
                'message': f'No valid resumes found in {resume_path.name}'
            })
        
        # Rank candidates
        job_requirements = {'required_skills': [], 'min_experience': 0}
        results = ranking_engine.rank_candidates(candidates, job_requirements)
        
        return jsonify({
            'success': True,
            'candidates': results,
            'total': len(results),
            'source': resume_path.name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/dashboard')
def dashboard():
    # Load analytics data
    analytics_path = 'data/processed/dashboard_analytics.json'
    if Path(analytics_path).exists():
        with open(analytics_path, 'r') as f:
            analytics = json.load(f)
    else:
        # Default empty analytics structure
        analytics = {
            'overview': {
                'total_candidates': 0,
                'average_score': 0.0,
                'score_range': {'min': 0, 'max': 0}
            },
            'skills_distribution': {'top_skills': []},
            'grade_distribution': {},
            'top_candidates': []
        }
    
    return render_template('dashboard.html', analytics=analytics)

@app.route('/api/analytics')
def get_analytics():
    analytics_path = 'data/processed/dashboard_analytics.json'
    if Path(analytics_path).exists():
        with open(analytics_path, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'No analytics data available'}), 404

@app.route('/api/visualizations/<chart_name>')
def get_visualization(chart_name):
    chart_path = f'data/visualizations/{chart_name}'
    if Path(chart_path).exists():
        return send_file(chart_path, mimetype='image/png')
    return jsonify({'error': 'Chart not found'}), 404

@app.route('/api/resumes')
def list_resumes():
    """List all available resumes"""
    import os
    base_dir = Path(os.getcwd())
    resumes = []
    
    # Check uploaded folder
    uploaded_path = base_dir / 'data/resumes/uploaded'
    if uploaded_path.exists():
        for file in uploaded_path.glob('*'):
            if file.suffix.lower() in ['.pdf', '.docx', '.txt']:
                resumes.append({
                    'filename': file.name,
                    'path': str(file),
                    'size': file.stat().st_size,
                    'source': 'uploaded'
                })
    
    # Check test folder
    test_path = base_dir / 'data/resumes/test'
    if test_path.exists():
        for file in test_path.glob('*'):
            if file.suffix.lower() in ['.pdf', '.docx', '.txt']:
                resumes.append({
                    'filename': file.name,
                    'path': str(file),
                    'size': file.stat().st_size,
                    'source': 'test'
                })
    
    return jsonify({'resumes': resumes, 'total': len(resumes)})

@app.route('/api/resume/<path:filename>')
def view_resume(filename):
    """View or download a specific resume"""
    import os
    base_dir = Path(os.getcwd())
    
    # Check uploaded folder first
    uploaded_path = base_dir / 'data/resumes/uploaded' / filename
    if uploaded_path.exists():
        return send_file(uploaded_path, mimetype='application/pdf' if filename.endswith('.pdf') else None)
    
    # Check test folder
    test_path = base_dir / 'data/resumes/test' / filename
    if test_path.exists():
        return send_file(test_path, mimetype='application/pdf' if filename.endswith('.pdf') else None)
    
@app.route('/api/resume/<path:filename>', methods=['DELETE'])
def delete_resume(filename):
    """Delete a specific resume"""
    import os
    base_dir = Path(os.getcwd())
    
    # Check uploaded folder first
    uploaded_path = base_dir / 'data/resumes/uploaded' / filename
    if uploaded_path.exists():
        uploaded_path.unlink()
        # Also delete JSON if exists
        json_path = base_dir / 'data/resumes/uploaded' / f"{filename}.json"
        if json_path.exists():
            json_path.unlink()
        return jsonify({'success': True, 'message': 'Resume deleted'})
    
    # Check test folder (only if not in uploaded)
    test_path = base_dir / 'data/resumes/test' / filename
    if test_path.exists():
        return jsonify({'success': False, 'error': 'Cannot delete test resumes'}), 403
    
    return jsonify({'success': False, 'error': 'Resume not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
