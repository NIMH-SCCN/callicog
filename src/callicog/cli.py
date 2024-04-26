import click

from callicog.marmobox_listener import _main as run_task_agent
# from callicog.main import callicog_run
# from callicog.main import callicog_resume


@click.group()
def callicog():
    """
    CalliCog operant chamber system command line interface.

    NIMH Section on Cellular and Cognitive Neurodevelopment
    """
    pass


@callicog.group()
def start():
    """Start specific Callicog components."""
    pass


@start.command()
@click.argument('port', default='ttyACM0')
@click.option('--width', default=1280, help='Width of the Psychopy window')
@click.option('--height', default=720, help='Height of the Psychopy window')
@click.option('--dummy', is_flag=True, help='No reward module')
@click.option('--fullscreen', is_flag=True, default=True, help='Psychopy window is fullscreen')
def agent(port, width, height, dummy, fullscreen):
    """
    Start a task agent to listen for, and run, commands from an executive machine.

    PORT: Arduino device port (e.g. "ttyACM0")


    Note: Intel NUCs may require the following setting:

      $ xrandr --output HDMI-2 --mode "1280x720"

    """
    click.echo("<<< stub: start callicog task agent aka listener >>>")
    # run_task_agent(port, width, height, dummy, fullscreen)


@start.command()
@click.argument("host", default="0.0.0.0")
@click.option("-p", "--port", default=5000)
@click.option("--debug", default=True)
def webapp(host, port, debug):
    """
    Start the CalliCog web server (Flask).
    """
    from callicog.webapp.flask_app import app
    app.run(host=host, port=port, debug=debug)


def _demo(height=800, width=600, arduino_port='dummy'):
    from callicog.tasks.touch2 import TaskInterface
    from callicog.marmobox_interface import MarmoboxInterface
    window_size = (height, width)
    is_dummy = True if arduino_port == 'dummy' else False
    is_fullscreen = False
    touch2 = TaskInterface()
    touch2.generate_trials()
    trial_agent = MarmoboxInterface(arduino_port, window_size, is_dummy, is_fullscreen)
    trial_agent.initialize()
    for trial_params in touch2.trials:
        trial_windows = touch2.build_trial(trial_params)
        #assert trial_windows[0].ppy_window
            #.mouseVisible in (True, False)
        semantically_different_trial_params = {'trial_windows': trial_windows}
        result = trial_agent.run_trial(semantically_different_trial_params)
    return result


@start.command()
def demo():
    """
    Locally run a demonstration task.
    """
    from pprint import pprint
    result = _demo()
    click.echo(pprint(result))


@callicog.command()
@click.argument('host', required=True)
@click.argument('animal', required=True)
@click.argument('template', required=True)
def run(host, animal, template):
    """
    Start a new experiment.

    HOST: hostname or IP address of CalliCog

    ANIMAL: name of animal participating in the experiment

    TEMPLATE: name of experiment template

    !!! Important !!!
    The animal and the template must already exist in the database. If they
    don't yet, create them via the CalliCog webapp.
    """
    click.echo(f"RUN new {template} experiment with {animal} on {host}")
    # TODO: fix conflict with argparse and break args obj coupling
    # callicog_run(host, animal, template)


@callicog.command()
@click.argument('host', required=True)
@click.argument('experiment', required=True, type=int)
def resume(host, animal, template):
    """
    Resume an existing experiment.

    HOST: hostname or IP address of CalliCog

    EXPERIMENT: integer id of experiment to resume

    If you don't know the experiment id, find it using the CalliCog webapp.
    """
    click.echo(f"RESUME experiment {experiment} on {host}")
    # TODO: fix conflict with argparse and break args obj coupling
    # callicog_resume(host, experiment)


if __name__ == "__main__":
    callicog()
