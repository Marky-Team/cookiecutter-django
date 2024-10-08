"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: restrict Cookiecutter Django project initialization
      to Python 3.x environments only
"""

from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

# The content of this string is evaluated by Jinja, and plays an important role.
# It updates the cookiecutter context to trim leading and trailing spaces
# from domain/email values
"""
{{ cookiecutter.update({ "domain_name": cookiecutter.domain_name | trim }) }}
"""

python_package_name = "{{ cookiecutter.python_package_name }}"
if hasattr(python_package_name, "isidentifier"):
    assert python_package_name.isidentifier(), "'{}' project slug is not a valid Python identifier.".format(python_package_name)

assert python_package_name == python_package_name.lower(), "'{}' project slug should be all lowercase".format(python_package_name)

assert "\\" not in "MyMarky, Incorporated", "Don't include backslashes in author name."
