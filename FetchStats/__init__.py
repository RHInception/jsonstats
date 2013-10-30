class PluginMount(type):
    """
    This idea was lifted from
    http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    """
    def __init__(cls, name, bases, attrs):
        print "Trying to create something new here..."
        print cls
        print

        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        """
        Returns a list of initialized plugin objects
        """
        return [p(*args, **kwargs) for p in cls.plugins]


class Fetcher:
    """
    Base class for fetching data.

    TODO:

    - Define a method to interrogate the Fetcher class to discover
    what additional REST endpoints a specific Fetcher may expose such
    that it may invoked directly and optionally with parameters.

    ex: /facter/(KEY)

    - Expose a method to manually refresh data

    - Create a common caching system
    """
    __metaclass__ = PluginMount
    import json
    import commands

    def dump_json(self, key=None):
        """
        Turn results in to json.
        """
        raise NotImplementedError('dump_json must be defined')

    def _load_data(self):
        """
        In this method you should load and then save all of your
        returnable into an instance variable.

        This method may be called to manually refresh a loaded fact
        plugin.
        """
        raise NotImplementedError('_load_data must be defined')

    def _exec(self, cmd=['true']):
        """
        Utility method for executing an arbitraty command in a shell

        `cmd` - Command to execute, given as a list

        returns a tuple of (return_status, command_output)
        """
        return self.commands.getstatusoutput(' '.join(cmd))
