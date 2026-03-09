import os
import sqlite3
import random
from flask import Flask, render_template

app = Flask(__name__)

# --- 1. 配置模块 (2026年生肖五行) ---
ZODIAC_2026 = {
    "马": [1, 13, 25, 37, 49], "蛇": [2, 14, 26, 38], "龙": [3, 15, 27, 39],
    "兔": [4, 16, 28, 40], "虎": [5, 17, 29, 41], "牛": [6, 18, 30, 42],
    "鼠": [7, 19, 31, 43], "猪": [8, 20, 32, 44], "狗": [9, 21, 33, 45],
    "鸡": [10, 22, 34, 46], "猴": [11, 23, 35, 47], "羊": [12, 24, 36, 48]
}

def get_detail(num):
    num = int(num)
    zodiac = next((k for k, v in ZODIAC_2026.items() if num in v), "未知")
    return f"{zodiac}"

# --- 2. 数据库模块 (适配 Render Disk) ---
DB_DIR = '/opt/render/project/src/data' if os.environ.get('RENDER') else 'data'
DB_PATH = os.path.join(DB_DIR, 'lottery.db')

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, nums TEXT, sp INTEGER)")
    conn.close()

# --- 3. 路由逻辑 ---
@app.route('/')
def index():
    init_db()
    
    # 模拟最新开奖 (后续可扩展 scraper)
    data = {"date": "2026-03-09", "nums": [5, 12, 23, 34, 45, 48], "sp": 8}
    
    # 模拟 AI 预测
    pred = {
        "main": sorted(random.sample(range(1, 50), 6)),
        "special": random.randint(1, 49)
    }
    
    # 详情转换
    latest_info = [{"n": n, "d": get_detail(n)} for n in data['nums']]
    sp_info = {"n": data['sp'], "d": get_detail(data['sp'])}
    
    return render_template('index.html', date=data['date'], latest=latest_info, sp=sp_info, pred=pred)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
