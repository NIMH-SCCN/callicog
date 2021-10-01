from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from marmobox import Marmobox
import argparse
import yaml

parser = argparse.ArgumentParser(description='Marmobox client. \
	Connects to Marmobox server and stores data in local database.')
parser.add_argument('config_filename', help='Client configuration file.', type=str)
args = parser.parse_args()

config_stream = open(args.config_filename, 'r')
config = yaml.safe_load(config_stream)

db_engine = create_engine('postgresql:///%s' % config['DATABASE_NAME'], echo=False)
#db_engine = create_engine('postgresql://postgres:marmoset@35.244.76.212:5432/marmodb') # google cloud VM
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=db_engine)
db_session = DatabaseSession()

mb = Marmobox(config['MARMOBOX_HOST'], config['MARMOBOX_PORT'], db_session)
mb.connect()
print('Connected')

animal = mb.get_animal(config['ANIMAL_CODE'])
if animal:
	tasks = config['TASKS']

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
