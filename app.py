from flask import Flask, render_template, request
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

@app.route("/", methods = ['GET', 'POST'])
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

#@app.route("/tasklist")
#def list():
     

if __name__ == "__main__":
    app.run(debug=True,port=3000)