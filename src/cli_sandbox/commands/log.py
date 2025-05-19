import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_log(name: str, repeat: int, messages: list[str], file: str = "usage_log.json"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "repeat": repeat,
        "messages": messages
    }
    
    path = Path(file)
    logs = []
    
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                pass
    logs.append(log_entry)
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
        
def load_logs(file: str = "usage_log.json") -> list[dict]:
    path = Path(file)
    if not path.exists():
        return []
    
    with open(file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def convert_logs_to_csv(file: str = "usage_log.json") -> pd.DataFrame:
    path = Path(file)
    if not path.exists():
        return pd.DataFrame()
    
    with open(file, "r", encoding="utf-8") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return pd.DataFrame()
    
    # フラットなDataFrameに変換
    records = []
    for log in logs:
        for msg in log["messages"]:
            records.append({
                "timestamp": log["timestamp"],
                "name": log["name"],
                "repeat": log["repeat"],
                "message": msg
            })
    return pd.DataFrame(records)

def upload_logs_to_google_sheets(
    json_file="usage_log.json",
    spreadsheet_name="UsageLog"
):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "google-credentials.json", scope
        )
    client = gspread.authorize(creds)
    
    # スプレッドシートを開いて戦闘のシートを取得
    sheet = client.open(spreadsheet_name).sheet1
    
    # usage_log.jsonを読み込む
    path = Path(json_file)
    if not path.exists():
        return False
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return False
    
    # シートをクリアしてヘッダーを書き込み
    sheet.clear()
    sheet.append_row(["timestamp", "name", "repeat", "message"])
    
    # 各メッセージを1行ずつ書き込む
    for log in logs:
        for msg in log["messages"]:
            sheet.append_row([
                log["timestamp"],
                log["name"],
                log["repeat"],
                msg])
    return True    
        