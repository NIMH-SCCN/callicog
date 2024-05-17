#     _______  _______  ___      ___      ___   _______  _______  _______ 
#    |       ||   _   ||   |    |   |    |   | |       ||       ||       |
#    |       ||  |_|  ||   |    |   |    |   | |       ||   _   ||    ___|
#    |       ||       ||   |    |   |    |   | |       ||  | |  ||   | __ 
#    |      _||       ||   |___ |   |___ |   | |      _||  |_|  ||   ||  |
#    |     |_ |   _   ||       ||       ||   | |     |_ |       ||   |_| |
#    |_______||__| |__||_______||_______||___| |_______||_______||_______|
"""
CalliCog 
========

CalliCog is an open, adaptable, low-cost operant chamber platform for
neuroscience.

Full documentation is at < https://github.com/NIMH-SCCN/callicog >.

:copyright: None.
:license: CC0 1.0 Universal (public domain). See LICENSE for more details.
"""

# Set default logging handler to avoid "No handler found" warnings.
import logging
import logging.config
from logging import NullHandler

import warnings


from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)

logging.config.fileConfig('logging.ini')
logging.getLogger(__name__).addHandler(NullHandler())

# Suppress logging spam from matplotlib:
logging.getLogger("matplotlib").setLevel(logging.WARNING)

""" Add filter to suppress NumPy warnings emanating from PsychoPy, e.g.:

.venv/lib/python3.8/site-packages/psychopy/visual/helpers.py:243:
DeprecationWarning: `np.float` is a deprecated alias for the builtin `float`.
To silence this warning, use `float` by itself. Doing this will not modify any
behavior and is safe. If you specifically wanted the numpy scalar type, use
`np.float64` here.
  Deprecated in NumPy 1.20; for more details and guidance:
    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations
    np.float64, np.float, np.int, np.long}
"""
warnings.filterwarnings("ignore", category=DeprecationWarning, module="psychopy")
