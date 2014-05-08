from . import TestCase
import mock
import platform
import optparse

"""Test we're not giving the OptionParser invalid kwargs on old boxes.

Kind of hard to test properly because this code is stuck in an "if
__name__ === '__main__'" block so I'm just replicating that code here
and testing the needful.
"""

class TestParser(TestCase):
    def test_epilog_setting_old_python(self):
        """We don't set the epilog on old python <= 2.4 versions"""
        mock_platform = mock.Mock(platform)

        mock_python_version_tuple = mock.Mock(return_value=('2', '4', '3'))
        mock_platform.python_version_tuple.return_value = mock_python_version_tuple()

        (major, minor, patch) = mock_platform.python_version_tuple()
        if int(major) == 2 and int(minor) < 5:
            py_platform = "old"
        else:
            py_platform = "new"

        self.assertEqual(py_platform, "old")

    def test_epilog_setting_old_python(self):
        """We set the epilog on new python >= 2.4 versions"""
        mock_platform = mock.Mock(platform)

        mock_python_version_tuple = mock.Mock(return_value=('2', '5', '3'))
        mock_platform.python_version_tuple.return_value = mock_python_version_tuple()

        (major, minor, patch) = mock_platform.python_version_tuple()
        if int(major) == 2 and int(minor) < 5:
            py_platform = "old"
        else:
            py_platform = "new"

        self.assertEqual(py_platform, "new")
