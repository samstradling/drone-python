"""
This module contains utility functions for finding and parsing plugin
input during development or normal runtime.
"""
import sys
import json
import os


def get_input():
    """
    Look for input in argv, environ and stdin. De-serialize and return whatever
    we can find.

    :rtype: dict
    :return: A dictionary of parameters from Drone.
    :raises: ValueError if no valid input is found, since this is required
        for normal plugin operation.
    """

    if '--' in sys.argv:
        payload_str = _get_input_from_argv()
    elif 'DRONE_REPO_OWNER' in os.environ:
        payload_str = _get_input_from_env()
    else:
        payload_str = _get_input_from_stdin()
    return json.loads(payload_str)


def _get_input_from_stdin():
    """
    This is only used during plugin testing and development. Drone
    passes params in via argv.

    :rtype: str
    :return: The value passed to the plugin via stdin.
    :raises: :py:class:`ValueError` if nothing is passed in.
    """
    params = sys.stdin.read()
    if not params:
        raise ValueError("No plugin input was found in argv or stdin.")
    return params


def _get_input_from_argv():
    """
    Drone passes parameters in via argv under normal operation. These
    are started with a ``--``.

    :rtype: str
    :returns: The value passed to the plugin via argv.
    :raises: ValueError if we found a ``--`` delimeter but no
        subsequent JSON payload.
    """
    payload_index = sys.argv.index('--') + 1
    params = sys.argv[payload_index:]
    if not params:
        raise ValueError(
            "A JSON payload was expected after the -- delimiter, but none "
            "was found.")
    return ' '.join(params)


def _get_input_from_env():
    """
    Drone 0.8 passes parameters in via environment variables.

    :rtype: str
    :returns: The value passed to the plugin via environ.
    :raises: ValueError if environment variables are not found.
    """
    try:
        params = {
            'repo': {
                'owner': os.environ['DRONE_REPO_OWNER'],
                'name': os.environ['DRONE_REPO_NAME'],
                'full_name': os.environ['DRONE_REPO'],
                'link_url': os.environ['DRONE_REPO_LINK'],
                'clone_url': os.environ['DRONE_REMOTE_URL']
            },
            'build': {
                'number': os.environ['DRONE_BUILD_NUMBER'],
                'event': os.environ['DRONE_BUILD_EVENT'],
                'branch': os.environ['DRONE_BRANCH'],
                'commit': os.environ['DRONE_COMMIT'],
                'ref': os.environ['DRONE_COMMIT_REF'],
                'author': os.environ['DRONE_COMMIT_AUTHOR'],
                'author_email': os.environ['DRONE_COMMIT_AUTHOR_EMAIL']
            },
            'workspace': {
                'root': os.environ['DRONE_WORKSPACE'],
                'path': os.environ['DRONE_WORKSPACE']
            },
            'vargs': {
                key[7:].lower(): value
                for key, value in os.environ.items()
                if key.startswith('PLUGIN_')
            }
        }
    except KeyError:
        raise ValueError(
            "Envronment variables were misconfigured.")
    return json.dumps(params)
