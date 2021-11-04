from database import DatabaseSession
from marmobox import Marmobox
import argparse
#import yaml

MARMOBOX_PORT = 10000

def callicog_run(box, args):
	animal = box.get_animal(args.animal)
	template = box.get_template(args.template)
	if animal and template:
		return box.new_experiment(animal, template)
	return None

def callicog_resume(box, args):
	experiment = box.get_experiment(args.experiment)
	return experiment

parser = argparse.ArgumentParser(description='Marmobox client. \
	Connects to Marmobox server and stores data in local database.')
parser.add_argument('server', help='Callicog IP address.', type=str)
subparsers = parser.add_subparsers()

parser_run = subparsers.add_parser('run')
parser_run.add_argument('animal', type=str)
parser_run.add_argument('template', type=str)
parser_run.set_defaults(func=callicog_run)

parser_resume = subparsers.add_parser('resume')
parser_resume.add_argument('experiment', type=int)
parser_resume.set_defaults(func=callicog_resume)

args = parser.parse_args()

#parser.add_argument('config_filename', help='Client configuration file.', type=str)
#args = parser.parse_args()
#config_stream = open(args.config_filename, 'r')
#config = yaml.safe_load(config_stream)

#db_engine = create_engine('postgresql:///%s' % config['DATABASE_NAME'], echo=False)
#db_engine = create_engine('postgresql://postgres:marmoset@35.244.76.212:5432/marmodb') # google cloud VM
#DatabaseSession = sessionmaker()
#DatabaseSession.configure(bind=db_engine)
db_session = DatabaseSession()

mb = Marmobox(args.server, MARMOBOX_PORT, db_session)
mb.connect()
print('Connected')

experiment = args.func(mb, args)
if experiment:
	mb.continue_task_experiment(experiment)

#animal = mb.get_animal(config['ANIMAL_CODE'])
#if animal:
	#tasks = config['TASKS']

	# new experiment or open experiment and continue
	#if len(animal.experiments) > 0:
	#	experiment = animal.experiments[0]
	#else:
	#	experiment = mb.new_experiment(animal, tasks)

	# resume experiment? find from ID
	#experiment = mb.new_experiment(animal, tasks)
	#mb.continue_task_experiment(experiment)

mb.disconnect()
db_session.close()
print('mbox disconnected')
print('db session closed')
print('Done')
