import argparse
import json
import logging
import logging.config

from callicog.marmobox import Marmobox
from callicog.webapp.flask_app import (
    db,
    app,
)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

MARMOBOX_PORT = 10000
app.app_context().push()


def callicog_run(box, args):
    animal = box.get_animal(args.animal)
    template = box.get_template(args.template)
    if animal and template:
        return box.new_experiment(animal, template)
    return None


def callicog_resume(box, args):
    experiment = box.get_experiment(args.experiment)
    return experiment


# parser = argparse.ArgumentParser(description='Marmobox client. \
#     Connects to Marmobox server and stores data in local database.')
# parser.add_argument('server', help='Callicog IP address.', type=str)
# subparsers = parser.add_subparsers()
# 
# parser_run = subparsers.add_parser('run', help='Executes a new experiment.')
# parser_run.add_argument('animal', type=str)
# parser_run.add_argument('template', type=str)
# parser_run.set_defaults(func=callicog_run)
# 
# parser_resume = subparsers.add_parser(
#     'resume', help='Resumes an existing experiment.')
# parser_resume.add_argument('experiment', type=int)
# parser_resume.set_defaults(func=callicog_resume)
# 
# args = parser.parse_args()

# parser.add_argument(
#     'config_filename',
#     help='Client configuration file.',
#     type=str
# )
# args = parser.parse_args()
# config_stream = open(args.config_filename, 'r')
# config = yaml.safe_load(config_stream)

# db_engine = create_engine(
#     'postgresql:///%s' % config['DATABASE_NAME'],
#     echo=False
# )
# db_engine = create_engine(
#     'postgresql://postgres:marmoset@35.244.76.212:5432/marmodb'
# ) # google cloud VM
# DatabaseSession = sessionmaker()
# DatabaseSession.configure(bind=db_engine)

with Marmobox(args.server, MARMOBOX_PORT, db.session) as mb:
    mb.connect()

    # Get existing or create new experiment:
    experiment = args.func(mb, args)
    if experiment:
        while True:
            try:
                # Run (or resume) the experiment:
                mb.continue_task_experiment(experiment)
                # Experiment over, exit loop:
                break
            except json.JSONDecodeError as exc:
                # Due to networking errors, we have been seeing truncations of
                # JSON messages, leading to JSONDecodeErrors. If this happens,
                # log the error and automatically resume experiment:
                logger.error(
                    "Malformed JSON, presumably truncated due to packet loss. "
                    "Attempting to auto-resume..."
                )
                logger.error(str(exc))
                # Auto-resume the experiment, iterate the loop:
                continue

    # animal = mb.get_animal(config['ANIMAL_CODE'])
    # if animal:
        # tasks = config['TASKS']

        # new experiment or open experiment and continue
        # if len(animal.experiments) > 0:
        #     experiment = animal.experiments[0]
        # else:
        #     experiment = mb.new_experiment(animal, tasks)

        # resume experiment? find from ID
        # experiment = mb.new_experiment(animal, tasks)
        # mb.continue_task_experiment(experiment)

    db.session.close()
    logger.info('db session closed')
    print('Done')
