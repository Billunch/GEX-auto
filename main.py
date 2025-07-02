import os
import json
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 環境變數
google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")
google_sheet_id = os.environ.get("GOOGLE_SHEET_ID")

if not google_creds_json or not google_sheet_id:
    raise Exception("❌ GOOGLE_CREDENTIALS_JSON 或 GOOGLE_SHEET_ID 未正確設置")

# 驗證並連線 Google Sheet
creds_dict = json.loads(google_creds_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(google_sheet_id)

@app.route('/api/gex-log', methods=['POST'])
def log_gex_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Missing JSON"}), 400

    symbol = data.get("symbol")
    if not symbol:
        return jsonify({"status": "error", "message": "Missing symbol"}), 400

    try:
        worksheet = sheet.worksheet(symbol)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=symbol, rows="1000", cols="10")
        worksheet.append_row([
            "symbol", "call_wall", "put_wall", "gex_bias", "ai_signal",
            "confidence", "user_action", "actual_move", "strategy_result"
        ])

    worksheet.append_row([
        data.get("symbol", ""),
        data.get("call_wall", ""),
        data.get("put_wall", ""),
        data.get("gex_bias", ""),
        data.get("ai_signal", ""),
        data.get("confidence", ""),
        data.get("user_action", ""),
        data.get("actual_move", ""),
        data.get("strategy_result", "")
    ])

    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    return "✅ GEX Logger API Ready!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
