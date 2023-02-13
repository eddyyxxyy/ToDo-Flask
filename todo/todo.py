from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/meta')
def meta():
    return render_template('meta.html')

if __name__ == '__main__':
    app.run()
