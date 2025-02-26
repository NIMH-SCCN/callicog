# Optimizing Timings in CalliCog

CalliCog records timings for three critical events during experimentation:

- **Display time**. A stimulus, stimuli, or a blank window are presented.
- **Touch time**. The test subject makes physical contact with a stimulus.
- **Release time**. The test subject removes physical contact from a stimulus. 

These three times provide all timing information about the sequence of events within a given trial. However, it is important to note that any behavioral system will inherently have margins of temporal error.
Therefore, it is recommended that the user identifies sources of this error in each individual experimental setup. Some important considerations are discussed below.

## Considerations for display time and lag
Scripting languages like Python execute line-by-line, so there is a necessary delay between the presentation of a display window (executed in CalliCog function `run_window()` by the PsychoPy method `win.flip()`) and the function that times it in the following line of code.
`win.flip()` is designed to maximize display speed, as it does not rely on processing to draw windows, but rather “flips” pre-drawn windows from the back buffer to the visual display (see [here](https://psychopy.org/api/visual/window.html#psychopy.visual.Window.flip) for more info).
However, hardware limitations can affect the time between the execution of this function and the physical presentation of a stimulus.

- **Refresh rate**. The speed at which displays can visually update is constrained by the refresh rate. For the Lilliput touchscreen recommended for use in CalliCog, this is 60 Hz or spans of 16.67 ms. By default, `win.flip()` synchronizes flips to the refresh rate (V-Sync) before returning.
However, the presentation of a window on an LCD monitor is not instantaneous, often “flood filling” from top-to-bottom. Window flips are timed after the back buffer is released, so the physical presentation of the stimulus may lag.
- **Graphics processing**. The speed of the Agent PC to buffer windows for presentation depends on the GPU of the chosen device. This time may vary depending on the complexity of visual stimuli and/or background applications running in parallel.
The previously tested hardware for the Agent PC uses integrated Intel UHD graphics, and this could potentially be improved with a dedicated GPU.

Ultimately, if the application requires high temporal precision, the only way to define the lag between the call to flip the window and the physical presentation of a stimulus is by using physical hardware such as a photodiode.
Such sensors can time changes in screen luminance associated with the presentation of stimuli, and this can be subtracted from the timing recorded in Python to compute the temporal error.
While CalliCog does not provide direct support for this hardware, interested users should refer to commercial systems like the [Black Box Toolkit](https://www.blackboxtoolkit.com/index.html).

## Considerations for touch time
Temporal error may also exist between the time a test subject interacts with the physical display and the time that touch is registered by the code. The duration of error is typically much shorter than for display time and involves less variables, but it is still an important consideration for precision.

Touch inputs are detected by the CalliCog function `__wait_touch()`, which runs an empty loop to detect changes in input and then immediately time them. While the lag in this loop is negligible, the rate at which touch inputs can be received is limited by the touch sampling rate of the display.
For an example touchscreen with a touch sampling rate of 120 Hz, the potential error caused would be 0-8.3 ms.

Finally, it is worth mention that not all considerations for timing reliability are technical. In general, we recommend also paying close attention to the behavior of the test subject. Often, stimuli may be triggered unintentionally, or at a delayed time to what the test subject intended.
For example, marmosets may choose to interact with the touchscreen using either their muzzle or their hand. When muzzle touching, saliva may interrupt the sensitivity of the capacitive screen (imagine trying to use a cell phone in the rain) and therefore touch inputs may not align with the animal’s action.
Likewise, when hand touching, marmosets opt for a so-called “power grip” in which they touch with an open palm. This can sometimes result in touches from the animal’s nails, which do not reliably register input on capacitive screens.
The take-home: users should consider that the touch time from an animal may not always exactly match the time it executed an action, an important notion for neural recordings. 
