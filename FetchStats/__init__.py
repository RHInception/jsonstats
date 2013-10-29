__all__ = [
    'RPM',
    'Facter'
    ]

class Fetcher(object):
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
