from flask import Flask, render_template
from database import init_db, get_history
from scraper import fetch_latest
from predictor import get_ai_prediction
from config import get_detail
import os

app = Flask(__name__)

@app.route('/')
def index():
    init_db()
    data = fetch_latest()
    pred = get_ai_prediction()
    
    # 格式化最新开奖
    latest_info = [{"n": n, "d": get_detail(n)} for n in data['nums']]
    sp_info = {"n": data['sp'], "d": get_detail(data['sp'])}
    
    return render_template('index.html', date=data['date'], latest=latest_info, sp=sp_info, pred=pred)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)