# How to start the server and test it

In terminal 1:

    . ./hacking/setup-env
    ./server.py

In terminal 2:

    curl localhost:8888 | python -m json.tool


# How to make a new fact plugin


* New fact plugins MUST subclass the `Fetcher` parent class. Example:

        from FetchStats import Fetcher
        class MegaFRObber(Fetcher):


* New fact plugins MUST define the `dump` method. This MUST return a
  raw python datastructure which is serializable by the JSON
  module. Example

        def dump(self):
            return self.data


* New fact plugins MUST define the `dump_json` method. This method may
  return a serialized datastructure (most likely from `dump`) as a
  JSON string. Example:

        def dump_json(self):
            return self.json.dumps(self.dump())

* New fact plugins MUST define the `_load_data` method. This method
  may be called internally to refresh a given fact plugins cache.

* New fact plugins module names MUST be added to the `__all__` list in
  `FetchStats/Plugins/__init__.py`
