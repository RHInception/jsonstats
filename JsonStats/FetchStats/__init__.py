class PluginMount(type):
    """
    This idea was lifted from
    http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    """
    def __init__(cls, name, bases, attrs):
        print "Loading plugin... %s" % str(cls)

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
        instantiate_plugins = [p(*args, **kwargs) for p in cls.plugins]
        return [p for p in instantiate_plugins if p._state]


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
    try:
        import json
    except:
        import simplejson as json
    import commands

    _state = False
    context = 'Fetcher'

    def dump(self, key=None):
        """
        Return a raw datastructure. This return value is collected by
        the main REST interface and joined with all the other plugins
        output. Then that final datastructure is dumped as JSON
        """
        raise NotImplementedError('dump must be defined')

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

    def _exec(self, cmd='true'):
        """
        Utility method for executing an arbitraty command in a shell

        `cmd` - Command to execute, given as a string

        returns a string of command_output
        """
        (ret, out) = self.commands.getstatusoutput(cmd)
        if not ret == 0:
            raise OSError(out)
        else:
            return out

    def _loaded(self, state, msg=None):
        """
        Frob the state of the plugins `_state` attribute. This is
        used to notify about plugins which fail to load.

        Additionally, if a plugin fails to load, this will stop it
        from registering with the plugin mount.

        `state` - BOOL - True if the plugin loaded correctly, False
        otherwise

        `msg` - STRING - Required if `state` == False - Exception text
        or otherwise helpful error message about the failure
        """
        self._state = state

        if not self._state:
            print "ERROR: Failed to load plugin '%s':\n%s" % (self.context, msg)
