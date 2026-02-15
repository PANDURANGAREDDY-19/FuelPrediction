# Smart Recruitment System - Complete Documentation

## 🎯 Project Overview
AI-powered recruitment system with face recognition, resume parsing, candidate ranking, analytics, and web interface.

## ✅ All 5 Modules Complete

### Module 1: Face Recognition
- **Face Detection**: OpenCV Haar Cascade
- **Face Verification**: FaceNet embeddings
- **Custom Training**: MobileNetV2 (82 classes, 670 images)
- **Files**: `src/image_processing/`

### Module 2: Resume NLP
- **Parsing**: PDF/DOCX/TXT with pdfplumber, PyPDF2, python-docx
- **Entity Extraction**: Name, email, phone, LinkedIn, GitHub, location
- **Skill Extraction**: 70+ technical skills, 13 soft skills
- **Files**: `src/nlp_engine/`

### Module 3: Candidate Ranking
- **Scoring**: Skills (40%), Experience (30%), Education (20%), Completeness (10%)
- **Job Matching**: TF-IDF similarity
- **Grading**: A/B/C/D grades
- **Files**: `src/ranking/`

### Module 4: Analytics Dashboard
- **Statistics**: Overview, skills distribution, score distribution
- **Visualizations**: Grade charts, completeness charts (matplotlib)
- **Export**: JSON analytics data
- **Files**: `src/analytics/`

### Module 5: Web Interface
- **Framework**: Flask
- **Features**: Resume upload, face verification, ranking, analytics, resume management
- **API**: RESTful endpoints
- **Files**: `src/ui/`

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Launch Web Application
```bash
python run_app.py
```
Access at: http://127.0.0.1:5000

### Train Face Recognition Model
```bash
python reorganize_dataset.py  # Organize dataset
python train.py               # Train model
```

### Process Resumes
```bash
python batch_process_resumes.py  # Batch processing
# Results saved to data/processed/
```

## 📁 Project Structure
```
smart_recruitment_system/
├── src/
│   ├── image_processing/    # Module 1: Face recognition
│   ├── nlp_engine/          # Module 2: Resume parsing
│   ├── ranking/             # Module 3: Candidate ranking
│   ├── analytics/           # Module 4: Analytics
│   └── ui/                  # Module 5: Web interface
├── data/
│   ├── resumes/
│   │   ├── uploaded/        # User-uploaded resumes
│   │   └── test/            # Sample resumes
│   ├── processed/           # Training data & results
│   ├── uploads/             # Temporary uploads
│   └── visualizations/      # Generated charts
├── config/                  # Configuration files
├── run_app.py              # Launch web app
├── train.py                # Train face model
└── requirements.txt        # Dependencies
```

## 🌐 Web Interface Features

### Home Page (/)
- **Resume Upload**: Upload PDF/DOCX/TXT, auto-parse and store
- **Face Verification**: Upload photo, detect faces with OpenCV
- **Candidate Ranking**: Enter job description, rank all candidates
- **Resume Management**: View, download, delete uploaded resumes

### Analytics Dashboard (/dashboard)
- Total candidates, average score, highest score
- Grade distribution pie chart
- Profile completeness chart
- Top skills table
- Top candidates ranking

### API Endpoints
- `POST /upload_resume` - Upload and parse resume
- `POST /verify_face` - Face detection
- `POST /rank_candidates` - Rank candidates by job description
- `GET /api/resumes` - List all resumes
- `GET /api/resume/<filename>` - View resume in browser
- `DELETE /api/resume/<filename>` - Delete uploaded resume
- `GET /dashboard` - Analytics dashboard
- `GET /api/analytics` - Get analytics JSON
- `GET /api/visualizations/<chart>` - Get chart images

## 🔧 Key Scripts

### run_app.py
Launch Flask web application - **Main entry point for production**

### train.py
Train face recognition model with MobileNetV2

### reorganize_dataset.py
Organize face images for training

### batch_process_resumes.py
Process multiple resumes at once

## 📊 Data Flow

1. **Resume Upload** → Parse → Store in `data/resumes/uploaded/` + JSON cache
2. **Face Upload** → Detect with OpenCV → Return face count
3. **Ranking Request** → Load resumes → Parse → Score → Rank → Return results
4. **Analytics** → Load ranking results → Generate stats → Create charts → Display

## 🎨 Technologies

- **Backend**: Flask, Python 3.13
- **ML/DL**: TensorFlow, Keras, OpenCV, MTCNN
- **NLP**: PyPDF2, pdfplumber, python-docx, regex
- **Analytics**: matplotlib, scikit-learn
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## 📝 Configuration

Edit `config/settings.py`:
- Image size, confidence thresholds
- Model paths
- Scoring weights

## 🔒 Security Notes

- Test resumes cannot be deleted (protected)
- Only uploaded resumes can be removed
- File size limit: 16MB
- Supported formats: PDF, DOCX, TXT, JPG, PNG

## 🎯 Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.ui.app:app
```

## 📈 System Status
**✅ ALL 5 MODULES COMPLETE AND PRODUCTION-READY**

## 🆘 Troubleshooting

**Web app not loading?**
- Use http://127.0.0.1:5000 instead of localhost
- Check if port 5000 is available

**Resume parsing fails?**
- Ensure file is text-based PDF (not scanned image)
- Check file encoding for TXT files

**Face detection not working?**
- Install opencv-python: `pip install opencv-python`
- Ensure image has clear face visible

**Ranking returns no results?**
- Check resumes exist in `data/resumes/uploaded/` or `data/resumes/test/`
- Verify resumes are valid format

## 📧 Support
For issues, check error messages in browser console (F12) or Flask terminal output.
