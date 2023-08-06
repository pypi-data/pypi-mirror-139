"""Minimal implementation for `terality account configure`, that collects the user account ID.

This allows Terality to contact users who tried to use Terality from Python 3.6.
"""
# See the comment at the top-level of the `terality` package.
import argparse
from urllib import request
import json
import platform
import sys


TERALITY_API_URL = "https://api.terality2.com/v1"


def _make_arg_parser():
    parser = argparse.ArgumentParser(
        description="Terality client for Python 3.6 and older.",
        epilog="Run `terality account configure` to get started.",
    )
    subparsers = parser.add_subparsers()
    account_subparser = subparsers.add_parser("account", help="Configure your Terality account.")

    account_subparser.add_argument("action", choices=["configure"])
    account_subparser.add_argument("--email")
    account_subparser.add_argument("--api-key")
    account_subparser.add_argument("--overwrite")
    account_subparser.set_defaults(callback=_account_cli)

    return parser


class DispatchError(Exception):
    pass


def _error_message():
    return (
        "Unsupported Python version.\n\n"
        "Terality only supports Python 3.7 and newer.\n"
        "The current Python version is: " + platform.python_version() + ".\n"
        "Please upgrade your Python version and install Terality again."
    )


def _dispatch_error(email=None):
    print(_error_message())
    try:
        _send_error(email)
    except Exception:
        pass


def _send_error(email=None):
    payload = {
        "email": email,
        "python_version": platform.python_version(),
        "operating_system": platform.platform(),
        "reason": "unsupported Python version",
    }
    data = json.dumps(payload).encode()
    req = request.Request(
        TERALITY_API_URL + "/errors/install", data=data
    )  # this will make the method "POST"
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req) as resp:
        status_code = resp.getcode()
        if status_code != "200":
            raise DispatchError(
                "Got HTTP status " + status_code + " when reporting the installation error."
            )


def _account_cli(args):
    if args.action != "configure":
        raise ValueError("Only supported action is 'configure'")

    email = args.email
    if not email:
        email = input("Your email: ")

    _dispatch_error(email)


def main():
    parser = _make_arg_parser()
    args = parser.parse_args()
    if not hasattr(args, "callback"):
        parser.print_help()
        sys.exit(1)
    args.callback(args)


if __name__ == "__main__":
    main()
