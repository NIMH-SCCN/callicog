from flask import Flask
import sys
import csv
from datetime import datetime
from io import StringIO
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    make_response,
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import true
from sqlalchemy.sql.expression import text

# NOTE: amending `sys.path` is only needed for importing modules from other
# directories due to lack of a conventional Python package directory structure
sys.path.append('..')
from marmobox_schema import (
    db,
    Protocol,
    # Task,
    Animal,
    Template,
    TemplateProtocol,
    Experiment,
    search,
    # Trial,
    # TrialParameter,
    # ProtocolParameter,
    # StimulusObject,
    # WindowObject,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///marmodb'
app.config['SECRET_KEY'] = 'secret'
app.config['WERKZEUG_DEBUG_PIN'] = 'off'
db.init_app(app)

CORS(app)

DATE_FORMAT = '%d/%m/%Y'
TIME_FORMAT = '%H:%M:%S'


def isDateValid(datetime_string, format_string):
    try:
        datetime.strptime(datetime_string, format_string)
    except Exception:
        return False
    return True


@app.route('/animals', methods=['GET', 'POST'])
def getAnimalList():
    if request.method == 'GET':
        animals = db.session.query(Animal).order_by(Animal.animal_id).all()
        return render_template('animals.html', animals=animals)
    if request.method == 'POST':
        alias = request.form['animal_code']
        if alias != '':
            animal = Animal(animal_code=alias)
            db.session.add(animal)
            db.session.commit()
            # flash('New animal added successfully!')
        return redirect('/animals')


@app.route('/tasks', methods=['GET', 'POST'])
def getTaskList():
    if request.method == 'GET':
        tasks = db.session.query(Protocol).order_by(Protocol.protocol_id).all()
        return render_template('tasks.html', tasks=tasks)
    if request.method == 'POST':
        task_name = request.form['task_name']
        if task_name != '':
            task = Protocol(protocol_name=task_name)
            db.session.add(task)
            db.session.commit()
            # flash('New task added successfully!')
        return redirect('/tasks')


@app.route('/templates', methods=['GET', 'POST'])
def getTemplateList():
    if request.method == 'GET':
        templates = db.session.query(Template).order_by(Template.template_id).all()
        return render_template('templates.html', templates=templates)
    if request.method == 'POST':
        template_name = request.form['template_name']
        if template_name != '':
            template = Template(template_name=template_name)
            db.session.add(template)
            db.session.commit()
        return redirect('/templates')


@app.route('/trials', methods=['GET', 'POST'])
def getTrialQueryResults():
    if request.method == 'GET':
        return render_template('trials.html', trials=[])
    if request.method == 'POST':
        trial_id = request.form['trial_id']
        session_id = request.form['session_id']
        experiment_id = request.form['experiment_id']

        template_name = request.form['template_name']
        task_name = request.form['task_name']
        animal_code = request.form['animal_code']

        trial_start = request.form['trial_start']
        trial_end = request.form['trial_end']
        timeout = request.form['timeout']

        ntargets = request.form['ntargets']
        ndistractors = request.form['ndistractors']
        outcome = request.form['outcome']

        target_shape = request.form['target_shape']
        target_color = request.form['target_color']
        trial_delay = request.form['trial_delay']
        query_result = search(
            trial_id=trial_id,
            session_id=session_id,
            experiment_id=experiment_id,
            template_name=template_name,
            task_name=task_name,
            animal_code=animal_code,
            trial_start=trial_start,
            trial_end=trial_end,
            timeout=timeout,
            ntargets=ntargets,
            ndistractors=ndistractors,
            outcome=outcome,
            target_shape=target_shape,
            target_color=target_color,
            trial_delay=trial_delay,
        )
        action = request.form.get('action')
        if action == 'export':
            import csv
            from io import BytesIO
            from flask import send_file, make_response
            from io import StringIO
            si = StringIO()
            cw = csv.writer(si)
            cw.writerows(query_result)
            response = make_response(si.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
            response.headers['Content-type'] = "text/csv"
            return response
            try:
                with BytesIO() as f:
                    writer = csv.writer(f, quotechar='"')
                    for row in query_result:
                        writer.writerow(row)
                    return send_file(
                        f,
                        mimetype='text/csv',
                        download_name='Adjacency.csv',
                        as_attachment=True
                    )
            except Exception as exc:
                myex = exc
                import pdb; pdb.set_trace()
        elif action == 'search':
            return render_template('trials.html', trials=query_result)

    raise ValueError("Unexpected request state.")


@app.route('/experiments/detail/<int:id>', methods=['GET'])
def getExperimentDetails(id):
    query_exp = db.session.query(Experiment).filter(Experiment.experiment_id == id).all()
    if len(query_exp) > 0:
        experiment = query_exp[0]
        if request.method == 'GET':
            return render_template('experiment_details.html', experiment=experiment)


@app.route('/experiments', methods=['GET', 'POST'])
def getExperimentList():
    all_animals = db.session.query(Animal).all()
    all_templates = db.session.query(Template).all()
    if request.method == 'GET':
        experiments = db.session.query(Experiment).order_by(Experiment.experiment_start).all()
    if request.method == 'POST':
        animal_id = request.form['animal_id']
        template_id = request.form['template_id']
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date']
        end_time = request.form['end_time']
        experiment_id = request.form['experiment_id']

        start_format = DATE_FORMAT
        end_format = DATE_FORMAT
        if start_time == '':
            start_datetime = start_date
        else:
            start_datetime = (start_date + '-' + start_time)
            start_format = DATE_FORMAT + '-' + TIME_FORMAT
        if end_time == '':
            end_datetime = end_date
        else:
            end_datetime = (end_date + '-' + end_time)
            end_format = DATE_FORMAT + '-' + TIME_FORMAT

        if (start_datetime == '' or isDateValid(start_datetime, start_format)) and (end_datetime == '' or isDateValid(end_datetime, end_format)):
            experiments = db.session.query(Experiment).filter(
                (true() if animal_id == '0' else Experiment.animal_id == animal_id),
                (true() if template_id == '0' else Experiment.template_id == template_id),
                (true() if start_datetime == '' else Experiment.experiment_start >= datetime.strptime(start_datetime, start_format)),
                (true() if end_datetime == '' else Experiment.experiment_end <= datetime.strptime(end_datetime, end_format)),
                (true() if experiment_id == '' else Experiment.experiment_id == experiment_id)
            ).all()
        else:
            return redirect(request.url)
    return render_template('experiments.html', experiments=experiments, all_animals=all_animals, all_templates=all_templates)


@app.route('/experiments/save/<int:id>', methods=['GET'])
def saveExperiment(id):
    si = StringIO()
    cw = csv.writer(si)
    q = text('select * from get_experiment_data(:param_id);')
    query_result = db.session.execute(q, {'param_id': id})
    cw.writerow(query_result.keys())
    cw.writerows(query_result)
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=experiment_{id}_data.csv'
    response.headers["Content-type"] = "text/csv"
    return response


@app.route('/experiments/delete/<int:id>')
def deleteExperiment(id):
    query_task = db.session.query(Experiment).filter(Experiment.experiment_id == id).all()
    if len(query_task) > 0:
        experiment = query_task[0]
        db.session.delete(experiment)
        db.session.commit()
        return redirect('/experiments')


@app.route('/tasks/update/<int:id>', methods=['GET', 'POST'])
def updateTask(id):
    query_task = db.session.query(Protocol).filter(Protocol.protocol_id == id).all()
    if len(query_task) > 0:
        task = query_task[0]
        if request.method == 'POST':
            task.protocol_name = request.form['task_name']
            db.session.commit()
            return redirect('/tasks')
        if request.method == 'GET':
            return render_template('update_tasks.html', task=task)


@app.route('/animals/update/<int:id>', methods=['GET', 'POST'])
def updateAnimal(id):
    query_animal = db.session.query(Animal).filter(Animal.animal_id == id).all()
    if len(query_animal) > 0:
        animal = query_animal[0]
        if request.method == 'POST':
            animal.animal_code = request.form['animal_code']
            db.session.commit()
            return redirect('/animals')
        if request.method == 'GET':
            return render_template('update_animals.html', animal=animal)


@app.route('/templates/update/<int:id>', methods=['GET', 'POST'])
def updateTemplate(id):
    query_exp = db.session.query(Template).filter(Template.template_id == id).all()
    if len(query_exp) > 0:
        template = query_exp[0]
        if request.method == 'POST':
            template.template_name = request.form['template_name']
            db.session.commit()
            return redirect(request.url)
        if request.method == 'GET':
            template_protocols = template.protocols
            all_protocols = db.session.query(Protocol).all()
            return render_template(
                'update_templates.html',
                template=template,
                template_protocols=template_protocols,
                all_protocols=all_protocols,
            )


@app.route('/templates/update/tasks/update/<int:id>', methods=['GET', 'POST'])
def updateTemplateTask(id):
    query_task = db.session.query(TemplateProtocol).filter(TemplateProtocol.template_protocol_id == id).all()
    if len(query_task) > 0:
        template_protocol = query_task[0]
        if request.method == 'GET':
            all_protocols = db.session.query(Protocol).all()
            return render_template('update_template_tasks.html', template_protocol=template_protocol, all_protocols=all_protocols)
        if request.method == 'POST':
            protocol_id = request.form['protocol_id']
            query_protocol = db.session.query(Protocol).filter(Protocol.protocol_id == protocol_id).all()
            if len(query_protocol) > 0:
                progression_type = request.form['progression_type']
                protocol = query_protocol[0]

                template_protocol.progression = progression_type
                template_protocol.target_trials = None
                template_protocol.target_sessions = None
                template_protocol.success_rate = None
                template_protocol.rolling_window_size = None
                if progression_type == 'target_based':
                    template_protocol.target_trials = int(request.form['target_trials'])
                if progression_type == 'session_based':
                    template_protocol.target_trials = int(request.form['target_trials'])
                    template_protocol.target_sessions = int(request.form['target_sessions'])
                    template_protocol.success_rate = float(request.form['success_rate'])
                if progression_type == 'rolling_average':
                    template_protocol.success_rate = float(request.form['success_rate'])
                    template_protocol.rolling_window_size = int(request.form['rolling_window_size'])
                template_protocol.protocol = protocol
                db.session.commit()
                return redirect('/templates/update/%s' % template_protocol.template.template_id)


@app.route('/tasks/delete/<int:id>')
def deleteTask(id):
    query_task = db.session.query(Protocol).filter(Protocol.protocol_id == id).all()
    if len(query_task) > 0:
        task = query_task[0]
        db.session.delete(task)
        db.session.commit()
        return redirect('/tasks')


@app.route('/templates/delete/<int:id>')
def deleteTemplate(id):
    query_exp = db.session.query(Template).filter(Template.template_id == id).all()
    if len(query_exp) > 0:
        template = query_exp[0]
        db.session.delete(template)
        db.session.commit()
        return redirect('/templates')


@app.route('/templates/update/tasks/delete/<int:id>')
def deleteTemplateTask(id):
    query_task = db.session.query(TemplateProtocol).filter(TemplateProtocol.template_protocol_id == id).all()
    if len(query_task) > 0:
        template_protocol = query_task[0]
        template_id = template_protocol.template.template_id
        db.session.delete(template_protocol)
        db.session.commit()
        return redirect('/templates/update/%s' % template_id)


@app.route('/templates/add-task/<int:id>', methods=['POST'])
def addTaskToTemplate(id):
    query_exp = db.session.query(Template).filter(Template.template_id == id).all()
    if len(query_exp) > 0:
        template = query_exp[0]
        if request.method == 'POST':
            protocol_id = request.form['protocol_id']
            progression_type = request.form['progression_type']

            query_protocol = db.session.query(Protocol).filter(Protocol.protocol_id == protocol_id).all()
            if len(query_protocol) > 0:
                protocol = query_protocol[0]
                template_protocol = TemplateProtocol(task_order=0, progression=progression_type)
                if progression_type == 'target_based':
                    template_protocol.target_trials = int(request.form['target_trials'])
                if progression_type == 'session_based':
                    template_protocol.target_trials = int(request.form['target_trials'])
                    template_protocol.target_sessions = int(request.form['target_sessions'])
                    template_protocol.success_rate = float(request.form['success_rate'])
                if progression_type == 'rolling_average':
                    template_protocol.success_rate = float(request.form['success_rate'])
                    template_protocol.rolling_window_size = int(request.form['rolling_window_size'])

                template_protocol.protocol = protocol
                template_protocol.template = template
                template.protocols.append(template_protocol)
                db.session.add(template_protocol)
                db.session.commit()
                return redirect('/templates/update/%s' % id)


@app.route('/animals/delete/<int:id>')
def deleteAnimal(id):
    query_task = db.session.query(Animal).filter(Animal.animal_id == id).all()
    if len(query_task) > 0:
        animal = query_task[0]
        db.session.delete(animal)
        db.session.commit()
        return redirect('/animals')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
