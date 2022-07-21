from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'abc12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


# add the task
@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
        if request.form['content'] == '':
            flash("Task cannot be empty Enter something...!")
            return redirect("/")
    
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
        except:
            return "There was an issue task not added to database" 
    else:
        tasks = Todo.query.order_by(Todo.created_date).all()
        return render_template('index.html',tasks=tasks)


# update the task
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task_to_update = Todo.query.get(id)
    if request.method == 'POST':
        if request.form['content'] == '':
            flash("Task cannot be empty Enter something...!")
            return redirect("/")
            
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a Problem in updating the task"
    else:
        return render_template('update.html',task=task_to_update)



# delete the task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem in deleting a task"



if __name__ == '__main__':
    app.run(debug=True)