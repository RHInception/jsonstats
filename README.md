# How to start the server and test it

In terminal 1:

    . ./hacking/setup-env
    ./bin/jsonstatsd

In terminal 2:

    curl localhost:8008 | python -m json.tool


# How to make a new fact plugin


* New fact plugins MUST subclass the `Fetcher` parent class. Example:

        from FetchStats import Fetcher
        class MegaFrobber(Fetcher):


* Read the source for the `Fetcher` base class in
  `JsonStats/FetchStats/__init__.py` to see the remaining methods you
  must implement in your plugin.


* New fact plugins module names MUST be added to the `__all__` list in
  `FetchStats/Plugins/__init__.py`
