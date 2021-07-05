from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from marmobox import Marmobox

DATABASE_NAME = 'marmodb'
#MARMOBOX_HOST = '192.168.0.30'
#MARMOBOX_HOST = '118.138.89.213'
MARMOBOX_HOST = 'localhost'
MARMOBOX_PORT = 10000

db_engine = create_engine('postgresql:///%s' % DATABASE_NAME, echo=True)
#db_engine = create_engine('postgresql://postgres:marmoset@35.244.76.212:5432/marmodb') # google cloud VM
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=db_engine)
db_session = DatabaseSession()

mb = Marmobox(MARMOBOX_HOST, MARMOBOX_PORT, db_session)
mb.connect()
print('Connected')

#animal = db_session.query(Animal).filter(Animal.animal_code == 'MSIMD-2123').all()[0]
animal = mb.wait_for_animal()
tasks = [
			{
				'name': 'tasks.dmts',
				'progression': 'rolling_average'
			}
		]

# new experiment or open experiment and continue
if len(animal.experiments) > 0:
	experiment = animal.experiments[0]
else:
	experiment = mb.new_experiment(animal, tasks)

mb.continue_task_experiment(experiment)

mb.disconnect()
db_session.close()
print('mbox disconnected')
print('db session closed')
print('Done')


