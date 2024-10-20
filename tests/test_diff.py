import unittest
from yaml_diff import compare_dicts, compare_lists

class TestYamlDiff(unittest.TestCase):
    def setUp(self):

        self.current_state = {
            'spec': {'containers': [
                {'name': 'nginx', 'image': 'nginx:1.14.2', 'env': [{'name': 'DATABASE_HOST', 'value': 'db1.example.com'}]},
                {'name': 'redis', 'image': 'redis:5.0'}
            ], 'replicas': 1}
        }

        self.desired_state = {
            'spec': {'containers': [
                {'name': 'nginx', 'image': 'nginx:1.16.3', 'env': [{'name': 'DATABASE_HOST', 'value': 'db2.example.com'}, {'name': 'MESSAGE_BROKER_HOST', 'value': 'kfk1.example.com'}]},
                {'name': 'redis', 'image': 'redis:6.0'}
            ], 'replicas': 3}
        }

    def test_diff(self):
        removed, added, changed = compare_dicts(self.current_state, self.desired_state)
        self.assertIn('.spec.containers.nginx.env.MESSAGE_BROKER_HOST', added)
        self.assertEqual(len(changed), 4)

if __name__ == "__main__":
    unittest.main()
