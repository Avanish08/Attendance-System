import threading
import webview
from app import app

def start_flask():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    # Run Flask in a background thread
    threading.Thread(target=start_flask, daemon=True).start()
    
    # Create desktop window
    webview.create_window("College Attendance System", "http://127.0.0.1:5000")
    webview.start()
