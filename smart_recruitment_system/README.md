# Smart Recruitment System

## ✅ Complete AI-Powered Hiring Platform

### All 5 Modules Implemented

1. **Face Recognition** - OpenCV detection, FaceNet verification, custom MobileNetV2 training
2. **Resume NLP** - PDF/DOCX/TXT parsing, entity & skill extraction (70+ skills)
3. **Candidate Ranking** - Weighted scoring, TF-IDF job matching, A-D grading
4. **Analytics Dashboard** - Statistics, visualizations, JSON export
5. **Web Interface** - Flask app with upload, ranking, analytics, resume management

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch web application
python run_app.py

# Access at http://127.0.0.1:5000
```

## 📁 Project Structure

```
smart_recruitment_system/
├── src/
│   ├── image_processing/    # Module 1
│   ├── nlp_engine/          # Module 2
│   ├── ranking/             # Module 3
│   ├── analytics/           # Module 4
│   └── ui/                  # Module 5
├── data/
│   ├── resumes/uploaded/    # User uploads
│   ├── resumes/test/        # Sample data
│   └── visualizations/      # Charts
├── run_app.py              # Launch app
├── train.py                # Train face model
└── requirements.txt        # Dependencies
```

## 🌐 Web Features

- **Resume Upload**: Auto-parse and store PDF/DOCX/TXT
- **Face Verification**: OpenCV-based face detection
- **Candidate Ranking**: Job description matching
- **Analytics Dashboard**: Charts, stats, top candidates
- **Resume Management**: View, delete uploaded resumes

## 📊 API Endpoints

- `POST /upload_resume` - Upload & parse
- `POST /verify_face` - Face detection
- `POST /rank_candidates` - Rank by job
- `GET /api/resumes` - List all
- `GET /api/resume/<file>` - View in browser
- `DELETE /api/resume/<file>` - Delete
- `GET /dashboard` - Analytics

## 🔧 Key Scripts

- `run_app.py` - **Launch web app (main entry point)**
- `train.py` - Train face recognition model
- `reorganize_dataset.py` - Organize dataset for training
- `batch_process_resumes.py` - Batch process resumes

## 📈 Technologies

- Flask, TensorFlow, OpenCV, MTCNN
- PyPDF2, pdfplumber, python-docx
- matplotlib, scikit-learn

## 📝 Full Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for complete details.

## 🎯 Status

**✅ ALL 5 MODULES COMPLETE - PRODUCTION READY**
