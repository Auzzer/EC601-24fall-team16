from flask import Flask, render_template, redirect, url_for, session
import os
import pandas as pd

app = Flask(__name__, static_folder='/Users/lizhengyuan/PycharmProjects/EC601_project/static')
app.secret_key = 'very_secret_key'

fullfinetune_dir = '/Users/lizhengyuan/PycharmProjects/EC601_project/static/fullfinetune'
qlora_dir = '/Users/lizhengyuan/PycharmProjects/EC601_project/static/qlora'
fullfinetune_images = sorted([f for f in os.listdir(fullfinetune_dir) if f.endswith('.png')])
qlora_images = sorted([f for f in os.listdir(qlora_dir) if f.endswith('.png')])

csv_file = 'button_press_count.csv'

def init_csv():
    df = pd.DataFrame({'fullfinetune': [0], 'qlora': [0]})
    df.to_csv(csv_file, index=False)

@app.route('/')
def index():

    session['index'] = 0
    return redirect(url_for('show_images'))

@app.route('/show_images')
def show_images():
    index = session.get('index', 0)
    if index >= len(fullfinetune_images) or index >= len(qlora_images):
        df = pd.read_csv(csv_file)
        return render_template('thankyou.html', fullfinetune_count=df['fullfinetune'][0], qlora_count=df['qlora'][0])
    fullfinetune_image = url_for('static', filename=f'fullfinetune/{fullfinetune_images[index]}')
    qlora_image = url_for('static', filename=f'qlora/{qlora_images[index]}')
    return render_template('index.html', fullfinetune_image=fullfinetune_image, qlora_image=qlora_image)

@app.route('/record_choice/<model>', methods=['POST'])
def record_choice(model):
    if 'index' in session:
        df = pd.read_csv(csv_file)
        df[model] += 1
        df.to_csv(csv_file, index=False)
        session['index'] = session.get('index', 0) + 1
    return redirect(url_for('show_images'))

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)