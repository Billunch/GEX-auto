from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# 掛載金鑰 JSON
GOOGLE_CREDS_JSON = json.loads(os.getenv("GOOGLE_CREDS_JSON"))

# 設定 Google Sheets 權限
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDS_JSON, scope)
client = gspread.authorize(creds)

# 打開試算表（記得換成你的網址 ID）
SHEET_ID = "1wJc7sC3432j1iagC5qK4WP-zUBwiSjGJQ2piEZdyDAI"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route("/", methods=["GET"])
def index():
    return "GEX Logger is running."

@app.route("/api/gex-log", methods=["POST"])
def gex_log():
    try:
        data = request.get_json()
        print("✅ 收到資料:", data)

        row = [
            data.get("symbol", ""),
            data.get("call_wall", ""),
            data.get("put_wall", ""),
            data.get("gex_bias", ""),
            data.get("ai_signal", ""),
            data.get("confidence", ""),
            data.get("user_action", ""),
            data.get("actual_move", ""),
            data.get("strategy_result", ""),
        ]

        print("📤 寫入資料:", row)
        sheet.append_row(row, value_input_option="USER_ENTERED")
        return jsonify({"status": "success"})

    except Exception as e:
        print("❌ 錯誤發生：", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
