

class Fetcher(object):
    """
    Base class for fetching data.
    """

    import json

    def dump_json(self, key=None):
        """
        Turn results in to json.
        """
        raise NotImplementedError('dump_json must be defined')
