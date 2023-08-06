"""Terality module for Python 3.6.

Terality doesn't support Python 3.6. However, the error displayed by pip is very hard to understand when
there's no package for a given Python version.

So, we publish this stub package for Python 3.6 and older.

For Python 3.7 and more recent, pip will select the main Terality package instead of this stub package.
"""
# If a user tries to install Terality on
# Python 3.6, she will get this stub package instead of an unclear pip error. The role of this stub package is:
# * to mock the "terality account configure" process to be able to collect the user account ID, so we can
#   contact her.
# * display a clean error asking the user to upgrade to Python 3.7 or more recent.
#
# To limit installation issues, this package should have as few dependencies as possible. Currently, it only
# depends on the Python 3 standard lib.
#
# This package must support Python 3.2 and newer, up to Python 3.6. This means no type annotations, no
# dataclasses, no f-strings... be careful about that!

import platform


def _error_message():
    return (
        "Unsupported Python version.\n\n"
        "Terality only supports Python 3.7 and newer.\n"
        "The current Python version is: " + platform.python_version() + ".\n"
        "Please upgrade your Python version and install Terality again."
    )


raise ImportError(_error_message())
