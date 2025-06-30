# GEX Logger Plugin

一個可部署到 Render 的 Plugin，用來接收 GEX 分析結果並寫入指定的 Google Sheets。

## 安裝套件
```
pip install -r requirements.txt
```

## 啟動服務
```
python main.py
```

## Google Sheets 設定
- 將 Service Account 的 credentials.json 放在專案根目錄
- 並分享表單編輯權限給該帳號
