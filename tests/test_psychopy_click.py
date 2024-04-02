import logging
import pytest

from datetime import datetime
from psychopy import core as ppy_core, visual, event
from psychopy.hardware import keyboard


# This library is noisy so let's ignore it unless it throws WARNING or above
logging.getLogger('PIL').setLevel(logging.WARNING)


@pytest.fixture(scope='session', autouse=True)
def core():
    yield ppy_core
    try:
        ppy_core.quit()
    except SystemExit:
        pass


@pytest.fixture
def win():
    """Creates a PsychoPy window for the test"""
    size = (800, 600)
    win = visual.Window(size=size, fullscr=False, units='pix')
    yield win
    win.close()


@pytest.fixture
def mouse(win):
    mouse = event.Mouse(win=win, visible=True)
    return mouse


def test_touch2():
    from tasks.touch2 import TaskInterface
    from marmobox_interface import MarmoboxInterface
    arduino_port = 'dummy'
    window_size = (800, 600)
    is_dummy = True
    is_fullscreen = False
    touch2 = TaskInterface()
    touch2.generate_trials()
    trial_agent = MarmoboxInterface(arduino_port, window_size, is_dummy, is_fullscreen)
    trial_agent.initialize()
    for trial_params in touch2.trials:
        trial_windows = touch2.build_trial(trial_params)
        assert trial_windows[0].ppy_window
            #.mouseVisible in (True, False)
        semantically_different_trial_params = {'trial_windows': trial_windows}
        result = trial_agent.run_trial(semantically_different_trial_params)
    # import pdb; pdb.set_trace()


@pytest.mark.skip
def test_stimulus_click(core, win, mouse):
    """Tests if a click occurs within the stimulus area"""

    # Define stimulus properties
    stim_radius = 100  # Change this to your desired radius
    stim_pos = (0, 0)   # Change this to your desired position

    # Create stimulus
    stim = visual.Circle(win, radius=stim_radius, pos=stim_pos, lineColor='red', fillColor='black')

    # Clear any existing events
    core.wait(0)
    event.clearEvents()

    start = datetime.now()
    elapsed = start - start
    timelimit = 60
    stim_clicked = False
    while elapsed.total_seconds() < timelimit:
        # Draw stimulus and wait for click
        stim.draw()
        win.flip()
        # buttons, times = mouse.getPressed(getTime=True)
        if mouse.isPressedIn(stim):
            stim_clicked = True
        elapsed = datetime.now() - start
    assert stim_clicked

    # Check if click occurred within stimulus boundaries
    # click_x, click_y, _ = click_loc
    # distance = ((click_x - stim_pos[0])**2 + (click_y - stim_pos[1])**2)**0.5
    # import pdb; pdb.set_trace()
    # assert distance <= stim_radius, "Click occurred outside stimulus area"


@pytest.mark.skip
def test_demo():
    """ Test implementation of tutorial example from psychopy.org:

    https://www.psychopy.org/coder/tutorial1.html

    Terminates on keypress.
    """
    try:
        #create a window
        mywin = visual.Window([800,600],monitor="testMonitor", units="deg")

        #create some stimuli
        grating = visual.GratingStim(win=mywin, mask='circle', size=3, pos=[-4,0], sf=3)
        fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)

        #create a keyboard component
        kb = keyboard.Keyboard()

        #draw the stimuli and update the window
        while True: #this creates a never-ending loop
            grating.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
            grating.draw()
            fixation.draw()
            mywin.flip()

            if len(kb.getKeys()) > 0:
                assert True
                break
            event.clearEvents()
    finally:
        #cleanup
        mywin.close()
