## HOW TO MAKE A NEW FACT PLUGIN:



* New fact plugins MUST have a class inside of them matching the file
  name exactly. Example:

  * `MegaFRObber.py` defines the class `MegaFRObber`

* New fact plugins MUST subclass the `Fetcher` parent class. Example:

    from FetchStats import Fetcher
    class MegaFRObber(Fetcher):

* New fact plugins MUST define the `dump_json` method. This method may
  return any valid datastructure which is serializable by the JSON
  module.

* New fact plugins MUST define the `_load_data` method. This method
  may be called internally to refresh a given fact plugins cache.
