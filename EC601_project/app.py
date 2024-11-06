from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

csv_file = "results.csv"

# 初始化 CSV 文件，确保它存在且包含正确的列头
def init_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=['Choice'])
        df.to_csv(csv_file, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_choice/<model>', methods=['POST'])
def record_choice(model):
    choice = 0 if model == 'fullfinetune' else 1
    # 读取或初始化 DataFrame
    try:
        results = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        results = pd.DataFrame(columns=['Choice'])

    # 添加新记录并计算平均值
    results = results.append({'Choice': choice}, ignore_index=True)
    results.to_csv(csv_file, index=False)  # 保存结果
    average = results['Choice'].mean()  # 计算平均值

    # 将平均值也存储到文件（或其他处理方式，视需求而定）
    with open(csv_file, "a") as f:
        f.write(f"Average,{average}\n")

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_csv()  # 确保在运行前 CSV 文件已经准备好
    app.run(debug=True)