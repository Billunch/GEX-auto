from flask import Flask, request, jsonify
from gspread_handler import write_to_sheet

app = Flask(__name__)

@app.route('/api/gex-log', methods=['POST'])
def log_gex_data():
    data = request.get_json()
    success = write_to_sheet(data)
    if success:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 500

@app.route('/')
def home():
    return "✅ GEX Logger is running.", 200

# 關鍵：綁定 0.0.0.0 與 PORT，供 Render 偵測
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
