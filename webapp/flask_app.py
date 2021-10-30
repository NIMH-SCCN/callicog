import sys
sys.path.append('..')

from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from database import DatabaseSession
from marmobox_schema import Protocol, Task, Animal

db = DatabaseSession()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

CORS(app)
app.session = scoped_session(DatabaseSession, scopefunc=_app_ctx_stack.__ident_func__)

@app.route('/animals', methods=['GET', 'POST'])
def getAnimalList():
	if request.method == 'GET':
		animals = db.query(Animal).order_by(Animal.animal_id).all()
		return render_template('animals.html', animals=animals)
	if request.method == 'POST':
		alias = request.form['animal_code']
		if alias != '':
			animal = Animal(animal_code=alias)
			db.add(animal)
			db.commit()
			#flash('New animal added successfully!')
		return redirect('/animals')

@app.route('/tasks', methods=['GET', 'POST'])
def getTaskList():
	if request.method == 'GET':
		tasks = db.query(Protocol).order_by(Protocol.protocol_id).all()
		return render_template('tasks.html', tasks=tasks)
	if request.method == 'POST':
		task_name = request.form['task_name']
		if task_name != '':
			task = Protocol(protocol_name=task_name)
			db.add(task)
			db.commit()
			#flash('New task added successfully!')
		return redirect('/tasks')


@app.route('/trials', methods=['GET', 'POST'])
def getTrialQueryResults():
	if request.method == 'GET':
		return render_template('tasks.html', tasks=[])
	if request.method == 'POST':
		animal_id = request.form['animal_id']
		task_id = request.form['task_id']
		experiment_id = request.form['experiment_id']
		if experiment_id == '':
			return render_template('tasks.html', tasks=[])
		
		tasks = db.query(Task).filter(Task.experiment_id == experiment_id).all()
		return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/update/<int:id>', methods=['GET', 'POST'])
def updateTask(id):
	query_task = db.query(Protocol).filter(Protocol.protocol_id == id).all()
	if len(query_task) > 0:
		task = query_task[0]
		if request.method == 'POST':
			task.protocol_name = request.form['task_name']
			db.commit()
			return redirect('/tasks')
		if request.method == 'GET':
			return render_template('update_tasks.html', task=task)

@app.route('/animals/update/<int:id>', methods=['GET', 'POST'])
def updateAnimal(id):
	query_task = db.query(Animal).filter(Animal.animal_id == id).all()
	if len(query_task) > 0:
		animal = query_task[0]
		if request.method == 'POST':
			animal.animal_code = request.form['animal_code']
			db.commit()
			return redirect('/animals')
		if request.method == 'GET':
			return render_template('update_animals.html', animal=animal)

@app.route('/tasks/delete/<int:id>')
def deleteTask(id):
	query_task = db.query(Protocol).filter(Protocol.protocol_id == id).all()
	if len(query_task) > 0:
		task = query_task[0]
		db.delete(task)
		db.commit()
		return redirect('/tasks')

@app.route('/animals/delete/<int:id>')
def deleteAnimal(id):
	query_task = db.query(Animal).filter(Animal.animal_id == id).all()
	if len(query_task) > 0:
		animal = query_task[0]
		db.delete(animal)
		db.commit()
		return redirect('/animals')

app.run(host='localhost', port=5000)
