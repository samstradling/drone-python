import copy
import io
import json
import sys
import unittest
import os
from drone import plugin


class ArgvInputTestCase(unittest.TestCase):

    def setUp(self):
        # We are going to be mucking with this. Back it up for
        # later restoration.
        self.original_argv = copy.copy(sys.argv)

    def tearDown(self):
        sys.argv = self.original_argv

    def test_empty_payload(self):
        """
        ArgvInputTestCase: Call the plugin with no input at all.
        """
        # No payload was passed in. We can't do anything with this
        # aside from fail.
        sys.argv = ['some-plugin', '--']
        self.assertRaises(ValueError, plugin.get_input)

    def test_valid_payload(self):
        """
        ArgvInputTestCase: Call the plugin with a properly formed payload.
        """
        test_dict = {'test': 'hello'}
        sys.argv = ['some-plugin', '--', json.dumps(test_dict)]
        parsed_dict = plugin.get_input()
        # There should be no differences in the dicts.
        self.assertFalse(set(test_dict.keys()) ^ set(parsed_dict.keys()))


class StdinInputTestCase(unittest.TestCase):

    def setUp(self):
        self.stdin = sys.stdin

    def tearDown(self):
        sys.stdin = self.stdin

    def test_empty_payload(self):
        """
        StdinInputTestCase: Call the plugin with no input at all.
        """
        sys.stdin = io.StringIO()
        self.assertRaises(ValueError, plugin.get_input)

    def test_valid_payload(self):
        """
        StdinInputTestCase: Call the plugin with a properly formed payload.
        """
        s = u'{"test": "hello"}'
        sys.stdin = io.StringIO(s)
        self.assertEqual(plugin.get_input(), json.loads(s))


class EnvVarTestCase(unittest.TestCase):

    def setUp(self):
        self.env = os.environ

    def tearDown(self):
        os.environ = self.env

    def test_empty_payload(self):
        """
        EnvVarTestCase: Call the plugin with badly formed input.
        """
        os.environ = {'DRONE_REPO_OWNER': True}
        self.assertRaises(ValueError, plugin.get_input)

    def test_valid_payload(self):
        """
        EnvVarTestCase: Call the plugin with a properly formed payload.
        """
        s = {
            'DRONE_REPO_OWNER': 'DRONE_REPO_OWNER',
            'DRONE_REPO_NAME': 'DRONE_REPO_NAME',
            'DRONE_REPO': 'DRONE_REPO',
            'DRONE_REPO_LINK': 'DRONE_REPO_LINK',
            'DRONE_REMOTE_URL': 'DRONE_REMOTE_URL',
            'DRONE_BUILD_NUMBER': 'DRONE_BUILD_NUMBER',
            'DRONE_BUILD_EVENT': 'DRONE_BUILD_EVENT',
            'DRONE_BRANCH': 'DRONE_BRANCH',
            'DRONE_COMMIT': 'DRONE_COMMIT',
            'DRONE_COMMIT_REF': 'DRONE_COMMIT_REF',
            'DRONE_COMMIT_AUTHOR': 'DRONE_COMMIT_AUTHOR_EMAIL',
            'DRONE_COMMIT_AUTHOR_EMAIL': 'DRONE_COMMIT_AUTHOR_EMAIL',
            'DRONE_WORKSPACE': 'DRONE_WORKSPACE',
            'PLUGIN_VARARGS_1': 'PLUGIN_VARARGS1',
            'PLUGIN_VARARGS_A': 'PLUGIN_VARARGS1'
        }
        r = {
            'repo': {
                'owner': s['DRONE_REPO_OWNER'],
                'name': s['DRONE_REPO_NAME'],
                'full_name': s['DRONE_REPO'],
                'link_url': s['DRONE_REPO_LINK'],
                'clone_url': s['DRONE_REMOTE_URL']
            },
            'build': {
                'number': s['DRONE_BUILD_NUMBER'],
                'event': s['DRONE_BUILD_EVENT'],
                'branch': s['DRONE_BRANCH'],
                'commit': s['DRONE_COMMIT'],
                'ref': s['DRONE_COMMIT_REF'],
                'author': s['DRONE_COMMIT_AUTHOR'],
                'author_email': s['DRONE_COMMIT_AUTHOR_EMAIL']
            },
            'workspace': {
                'root': s['DRONE_WORKSPACE'],
                'path': s['DRONE_WORKSPACE']
            },
            'vargs': {
                'varargs_1': s['PLUGIN_VARARGS_1'],
                'varargs_a': s['PLUGIN_VARARGS_A']
            }
        }
        os.environ = s
        self.assertEqual(plugin.get_input(), r)


if __name__ == '__main__':
    unittest.main()
