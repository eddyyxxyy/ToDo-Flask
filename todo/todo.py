import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    additional_info = db.Column(db.String(500))
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    modified = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

@app.route('/')
def home() -> str:
    todo_list = Todo.query.all()
    return render_template('home.html', todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get('title')
    additional_info = request.form.get('additional_info')
    new_todo = Todo(title=title, additional_info=additional_info)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    todo.modified = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/remove/<int:todo_id>')
def remove(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))
    

@app.route('/meta')
def meta() -> str:
    return render_template('meta.html')

if __name__ == '__main__':
    db.create_all()
    app.run()
