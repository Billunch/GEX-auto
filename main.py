from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import traceback

app = Flask(__name__)

# Google Sheets 認證設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")

if not creds_json:
    raise Exception("❌ 環境變數 GOOGLE_SHEETS_CREDENTIALS_JSON 未設置")

import json
creds_dict = json.loads(creds_json)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Google Sheets 文件 ID（你可以改成自己的）
sheet_id = os.environ.get("GOOGLE_SHEET_ID")  # 請記得設定這個環境變數！
sheet = client.open_by_key(sheet_id)

@app.route('/')
def home():
    return "✅ GEX Logger 正常運作中"

@app.route('/api/gex-log', methods=['POST'])
def log_gex_data():
    try:
        data = request.get_json()

        # 取得股票代碼對應的工作表（如不存在會報錯）
        symbol = data["symbol"]
        worksheet = sheet.worksheet(symbol)

        # 將資料寫入新列
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

        return jsonify({'status': 'success'})
    
    except Exception as e:
        print("❌ 發生錯誤：", str(e))
        traceback.print_exc()
        return jsonify({'status': 'error'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
