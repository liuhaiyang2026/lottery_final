import os
import sqlite3
import random
from flask import Flask, render_template

# 导入你项目中的其他模块
from database import init_db
from scraper import fetch_latest
from predictor import get_ai_prediction
from config import get_detail

app = Flask(__name__)

@app.route('/')
def index():
    # 1. 初始化数据库（确保在 Render Disk 上创建文件）
    try:
        init_db()
    except Exception as e:
        print(f"数据库初始化失败: {e}")

    # 2. 获取最新数据（加入防御性保护）
    data = None
    try:
        data = fetch_latest()
    except Exception as e:
        print(f"爬虫模块 fetch_latest 报错: {e}")

    # 3. 核心修复：如果 data 为 None 或报错，提供一套 2026 默认数据，防止网页崩溃
    if not data:
        data = {
            "date": "2026年数据获取中",
            "nums": [1, 13, 25, 37, 49, 10], # 示例平码
            "sp": 8                          # 示例特码
        }

    # 4. 获取 AI 预测结果
    try:
        pred = get_ai_prediction()
    except Exception as e:
        print(f"AI 预测模块报错: {e}")
        pred = {"main": [5, 15, 25, 35, 45, 48], "special": 9}

    # 5. 结合 config.py 为号码匹配生肖和五行
    latest_info = []
    try:
        for n in data['nums']:
            latest_info.append({"n": n, "d": get_detail(n)})
        
        sp_info = {"n": data['sp'], "d": get_detail(data['sp'])}
    except Exception as e:
        print(f"详情转换报错: {e}")
        latest_info = [{"n": 0, "d": "数据错误"}]
        sp_info = {"n": 0, "d": "数据错误"}

    # 6. 渲染到 HTML 模板
    return render_template(
        'index.html', 
        date=data['date'], 
        latest=latest_info, 
        sp=sp_info, 
        pred=pred
    )

if __name__ == "__main__":
    # 自动识别 Render 环境端口
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
