import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = "1wJc7sC3432j1iagC5qK4WP-zUBwiSjGJQ2piEZdyDAI"
SHEET_NAME = "工作表1"  # 依實際名稱修改

def write_to_sheet(data):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            now,
            data.get("symbol", ""),
            data.get("call_wall", ""),
            data.get("put_wall", ""),
            data.get("gex_bias", ""),
            data.get("ai_signal", ""),
            data.get("confidence", ""),
            data.get("user_action", ""),
            data.get("actual_move", ""),
            data.get("strategy_result", "")
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        print("❌ Failed to write to sheet:", e)
        return False
