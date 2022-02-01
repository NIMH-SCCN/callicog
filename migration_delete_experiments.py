from database import DatabaseSession
from marmobox_schema import Experiment, Animal

db = DatabaseSession()

del_experiments = db.query(Experiment).filter(Experiment.animal_id == 1).all()
if len(del_experiments):
	for experiment in del_experiments:
		db.delete(experiment)

db.commit()
db.close()
print('deleted')
