from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    mail = db.Column(db.String(100)) 
    msg = db.Column(db.String(500))

    def __init__(self, name, phone, mail, msg) -> None:
        self.name = name
        self.phone = phone
        self.mail = mail
        self.msg = msg

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/data', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = Data(request.form['name'], request.form['phone'],
        request.form['mail'], request.form['msg'])
        db.session.add(data)
        db.session.commit()
        return redirect('/')
    return redirect('/')


@app.route('/feed_data', methods=['GET', 'POST'])
def fetch():
    return render_template('data.html', data = Data.query.all())

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)