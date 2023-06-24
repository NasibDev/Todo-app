from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db = SQLAlchemy(app)



class todo(db.Model):
    slNo= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable =False)
    date_created= db.Column(db.DateTime, default= datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.slNo} - {self.title}"

@app.route("/", methods= ['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        description =request.form['description']
        Todo = todo(title= title, description = description)
        db.session.add(Todo)
        db.session.commit()

    allTodo= todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    


@app.route("/update/<int:slNo>", methods= ['GET', 'POST'])
def update(slNo):
    if request.method=='POST':
        title= request.form['title']
        description= request.form['description']
        Todo= todo.query.filter_by(slNo=slNo).first()
        Todo.title= title
        Todo.description= description
        db.session.add(Todo)
        db.session.commit()
        return redirect("/")

    Todo= todo.query.filter_by(slNo=slNo).first()
    return render_template('update.html', Todo=Todo)


@app.route("/delete/<int:slNo>")
def delete(slNo):
    Todo= todo.query.filter_by(slNo=slNo).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
