from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
     sno = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(200), nullable=False)
     desc = db.Column(db.String(500), nullable=False)
     creation_date = db.Column(db.DateTime, default=datetime.utcnow)


     #def __repr__(self) -> str:
         #return f"{self.sno} - {self.title}"

with app.app_context():
        db.create_all()

#create task
@app.route('/', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
         title = request.form['title']
         desc = request.form['desc']  
         task = Task(title=title, desc=desc)
         db.session.add(task)
         db.session.commit()
    allTask = Task.query.all()
    #print(allTask)
    return render_template('index.html', allTask = allTask)

#delete task
@app.route('/delete/<int:sno>')
def delete(sno):
     task_delete = Task.query.filter_by(sno=sno).first()
     db.session.delete(task_delete)
     db.session.commit()
     return redirect("/")

#update task
@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
     if request.method == 'POST':
         title = request.form['title']
         desc = request.form['desc']  
         task_update = Task.query.filter_by(sno=sno).first()
         task_update.title = title
         task_update.desc = desc
         db.session.add(task_update)
         db.session.commit()
         return redirect('/')
          
     task_update = Task.query.filter_by(sno=sno).first()
     return render_template('update.html',task_update=task_update)
     

     

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)