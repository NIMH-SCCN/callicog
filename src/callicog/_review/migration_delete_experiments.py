from callicog.marmobox_schema import Experiment, Animal, db


del_experiments = db.session.query(Experiment).filter(Experiment.animal_id == 1).all()
if len(del_experiments):
	for experiment in del_experiments:
		db.session.delete(experiment)

db.session.commit()
db.session.close()
print('deleted')
