from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(200), nullable=False)  
    desc = db.Column(db.String(500), nullable=False)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            new_todo = Todo(title=title, desc=desc)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('hello_world'))
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)  # Use get_or_404 for better error handling
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect(url_for('hello_world'))
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)  # Use get_or_404 for better error handling
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
