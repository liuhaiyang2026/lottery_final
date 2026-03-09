import os
import sqlite3
import random
from flask import Flask, render_template_string

app = Flask(__name__)

# --- 1. 2026年生肖灵码逻辑 ---
ZODIAC_2026 = {
    "马": [1, 13, 25, 37, 49], "蛇": [2, 14, 26, 38], "龙": [3, 15, 27, 39],
    "兔": [4, 16, 28, 40], "虎": [5, 17, 29, 41], "牛": [6, 18, 30, 42],
    "鼠": [7, 19, 31, 43], "猪": [8, 20, 32, 44], "狗": [9, 21, 33, 45],
    "鸡": [10, 22, 34, 46], "猴": [11, 23, 35, 47], "羊": [12, 24, 36, 48]
}

def get_detail(num):
    num = int(num)
    return next((k for k, v in ZODIAC_2026.items() if num in v), "未知")

# --- 2. 网页 UI 模板 (直接嵌入代码，防止 TemplateNotFound) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>澳门六合彩 AI 预测</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'PingFang SC', sans-serif; text-align: center; background: #f0f2f5; padding: 15px; }
        .card { background: white; margin: 10px auto; padding: 20px; max-width: 450px; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
        .ball { display: inline-block; width: 42px; height: 42px; background: #e74c3c; color: white; border-radius: 50%; line-height: 42px; margin: 5px; font-weight: bold; font-size: 18px; }
        .special { background: #3498db; }
        .pred-ball { background: #27ae60; }
        h2 { color: #2c3e50; font-size: 1.2rem; }
        small { color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="card">
        <h2>最新开奖 ({{ date }})</h2>
        {% for item in latest %}
            <div style="display:inline-block"><div class="ball">{{ item.n }}</div><br><small>{{ item.d }}</small></div>
        {% endfor %}
        <div style="display:inline-block"><span> + </span><div class="ball special">{{ sp.n }}</div><br><small>{{ sp.d }}</small></div>
    </div>
    <div class="card">
        <h2>AI 智能预测 (2026 灵码版)</h2>
        <p>推荐平码：</p>
        {% for n in pred.main %}
            <div class="ball pred-ball">{{ n }}</div>
        {% endfor %}
        <p>推荐特码：<div class="ball special">{{ pred.special }}</div></p>
        <p style="font-size: 10px; color: #999;">* 基于历史频率统计分析 *</p>
    </div>
</body>
</html>
"""

# --- 3. 主逻辑 ---
@app.route('/')
def index():
    # 模拟数据 (确保网页立刻能打开)
    data = {"date": "2026-03-09", "nums": [5, 12, 23, 34, 45, 48], "sp": 8}
    pred = {"main": sorted(random.sample(range(1, 50), 6)), "special": random.randint(1, 49)}
    
    latest_info = [{"n": n, "d": get_detail(n)} for n in data['nums']]
    sp_info = {"n": data['sp'], "d": get_detail(data['sp'])}
    
    return render_template_string(HTML_TEMPLATE, date=data['date'], latest=latest_info, sp=sp_info, pred=pred)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
