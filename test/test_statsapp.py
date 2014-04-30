from . import TestCase
import JsonStats.Utils

class Utils(TestCase):
    def setUp(self):
        # test_dump_sorted_json_string
        self._expected_sorted_dict = '{"Monkey": "two legs","Zeebra": "four legs","bar": 2,"foo": 1}'
        self._unsorted_dict = {
            'foo': 1,
            'bar': 2,
            'Zeebra': 'four legs',
            'Monkey': 'two legs'
            }

    def test_dump_sorted_json_string(self):
        """
        Verify that the JSON formatted string returned is sorted
        """
        sorted_str = JsonStats.Utils.dump_sorted_json_string(self._unsorted_dict)

        self.assertEqual(self._expected_sorted_dict, sorted_str,
                         msg="Expected '%s', got '%s'" %
                         (self._expected_sorted_dict, sorted_str))
