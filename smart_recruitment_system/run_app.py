"""
Launch Smart Recruitment System Web Application
"""
from src.ui.app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🚀 SMART RECRUITMENT SYSTEM")
    print("="*60)
    print("\n📱 Starting web server...")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("📊 Dashboard: http://127.0.0.1:5000/dashboard")
    print("\n⚡ Press CTRL+C to stop\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
