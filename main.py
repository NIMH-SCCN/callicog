from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from marmobox import Marmobox
import argparse

DATABASE_NAME = 'marmodb'
#MARMOBOX_HOST = '192.168.0.30'
#MARMOBOX_HOST = '118.138.89.213'
#MARMOBOX_HOST = '49.127.81.144'
#MARMOBOX_HOST = 'localhost'
MARMOBOX_PORT = 10000

parser = argparse.ArgumentParser(description='Marmobox client. \
	Connects to Marmobox server and stores data in local database.')
parser.add_argument('host', help='Marmobox server IP address.', type=str)
args = parser.parse_args()

db_engine = create_engine('postgresql:///%s' % DATABASE_NAME, echo=False)
#db_engine = create_engine('postgresql://postgres:marmoset@35.244.76.212:5432/marmodb') # google cloud VM
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=db_engine)
db_session = DatabaseSession()

mb = Marmobox(args.host, MARMOBOX_PORT, db_session)
mb.connect()
print('Connected')

animal = mb.wait_for_animal()
if animal:
	tasks = [{ 'name': 'supertask', 'progression': 'target_based' }]

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


