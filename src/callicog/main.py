import argparse
import json
import logging
import logging.config

from callicog.marmobox import Marmobox
from callicog.webapp.flask_app import (
    db,
    app,
)

logger = logging.getLogger(__name__)

SOCKET_PORT = 10000
app.app_context().push()


def run_or_resume(
        host,
        animal_name=None,
        template_name=None,
        experiment_id=None,
        socket_port=SOCKET_PORT,
        db_session=db.session
    ):
    assert (animal_name and template_name) or experiment_id
    with Marmobox(host, socket_port, db_session) as box:
        if experiment_id:
            # Resume: get existing experiment
            experiment = box.get_experiment(experiment_id)
        else:
            # Run: create new experiment
            animal = box.get_animal(animal_name)
            template = box.get_template(template_name)
            experiment = box.new_experiment(animal, template)
        box.connect()

        if experiment:
            while True:
                try:
                    # Run (or resume) the experiment:
                    box.continue_task_experiment(experiment)
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

        db_session.close()
        logger.info('db session closed')
        print('Done')