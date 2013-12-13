try:
    import json
except:
    import simplejson as json


def dump_sorted_json_string(input, **kwargs):
    """
    Given a datastructure, return a JSON formatted string of it with
    all dictionary keys sorted.

    * `input` - arbitrary Python datastructure

    * `**kwargs` - Arbitrary keyword arguments to pass to the
      `json.dumps` method. For example, you might want to pass a
      custom :py:class:`json.JSONEncoder` class. See the docs for a
      complete list of the available parameters.

    * `json.dumps` docs - http://docs.python.org/2.7/library/json.html#json.dumps
    """
    return json.dumps(input, sort_keys=True, separators=(',', ': '), **kwargs)
