"""
All settings in this file should be used by some other settings file(s), and this should
be the only file that other settings files import things from (other than combined.py).
"""

import sys
from pathlib import Path

import environ

BASE_DIR = (
    Path(__file__).resolve(strict=True).parent.parent.parent
)  # Should be the `<project_root>/app/` folder
APPS_DIR = BASE_DIR
env = environ.Env()

ENABLE_DEBUG_TOOLBAR = env.bool("ENABLE_DEBUG_TOOLBAR", default=False)

IS_IN_TEST = bool("test" in sys.argv)
