import unittest
from yaml_diff import compare_dicts

class TestYamlDiff(unittest.TestCase):
    def setUp(self):

        self.current_state = {
            'spec': {
                'containers': [
                    {
                        'name': 'nginx',
                        'image': 'nginx:1.14.2',
                        'env': [
                            {'name': 'DATABASE_HOST', 'value': 'db1.example.com'},
                            {'name': 'DISCOVERY_SERVICE', 'value': 'loc.example.com'}
                        ]
                    },
                    {'name': 'redis', 'image': 'redis:5.0'}
                ],
                'replicas': 1
            }
        }

        self.desired_state = {
            'spec': {
                'containers': [
                    {
                        'name': 'nginx',
                        'image': 'nginx:1.16.3',
                        'env': [
                            {'name': 'DATABASE_HOST', 'value': 'db2.example.com'},
                            {'name': 'MESSAGE_BROKER_HOST', 'value': 'kfk1.example.com'}
                        ]
                    },
                    {'name': 'redis', 'image': 'redis:6.0'}
                ],
                'replicas': 3
            }
        }

    def test_diff(self):
        # Compare current and desired states
        removed, added, changed = compare_dicts(self.current_state, self.desired_state)

        # Check that added items are correctly identified
        self.assertIn('.spec.containers[nginx].env[MESSAGE_BROKER_HOST]', [list(add.keys())[0] for add in added])
        self.assertIn('.spec.containers[nginx].env[DATABASE_HOST].value', [chg['path'] for chg in changed])

        # Check number of changes
        self.assertEqual(len(removed), 1)  # DISCOVERY_SERVICE should be removed
        self.assertEqual(len(added), 1)    # MESSAGE_BROKER_HOST should be added
        self.assertEqual(len(changed), 4)  # Four changes: replicas, nginx image, DATABASE_HOST value, redis image

        # Check that specific items were removed
        self.assertIn('.spec.containers[nginx].env[DISCOVERY_SERVICE]', [list(rem.keys())[0] for rem in removed])

if __name__ == "__main__":
    unittest.main()
