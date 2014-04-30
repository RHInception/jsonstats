import fnmatch
import os
import os.path
import re
import sys
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


def load_extra_plugins(pathspec):
    """
    Load extra fact plugins from a user specified directory

    `pathspec` - A string of either: a single directory path, or a
    compound (colon separated) list of paths
    """
    # Collect names of loaded plugins so we have something to test
    # success/failure against
    loaded_plugins = []

    paths = pathspec.split(':')
    for path in paths:
        loaded_plugins.extend(_load_plugins_from_dir(path))

    return loaded_plugins


def _load_plugins_from_dir(path):
    """
    Load plugins from a given path
    """
    plugins = []
    loaded_plugins = []

    # Expand out any ~'s
    full_path = os.path.expanduser(path)

    # Check if the dir exists, by asking for forgiveness
    try:
        filtered = fnmatch.filter(os.listdir(path), '*.py')
        plugins.extend(filtered)
    except OSError:
        # Uhoh, the path we were given doesn't exist/can't be read...
        pass
    else:
        # We read in the plugin dir, so lets add it to the load path
        sys.path.insert(1, path)

    # Import the thing(s)
    for plugin in plugins:
        match = re.search('(?P<name>.*)(?P<ext>\.py$)', plugin)
        if match:
            try:
                __import__(match.group('name'), globals(), locals(), [], -1)
            except:
                pass
            else:
                loaded_plugins.append(match.group('name'))
    return loaded_plugins
