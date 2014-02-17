
import unittest


class TestCase(unittest.TestCase):
    """
    Parent TestCase to use for all tests.
    """
    pass

    def assertGreaterEqual(self, first, second, msg=None):
        """
        Test that first is respectively >= than second
        depending on the method name. If not, the test will fail.
        """
        if first >= second:
            pass
        else:
            self.fail(msg=msg)
