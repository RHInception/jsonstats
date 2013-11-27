# jsonstats
[![Build Status](https://travis-ci.org/tbielawa/jsonstats.png?branch=master)](https://travis-ci.org/tbielawa/jsonstats)

RESTful back end for querying arbitraty system "facts".

## Features
* Minimal set of requirements
* Python 2.4+ compatible
* Access and application logging
* host and environment REST endpoints
* Unit tested

### Requirements
* Python 2.4+
* [python-simplejson](https://pypi.python.org/pypi/simplejson/) if Python 2.4 or 2.5
* [PyYAML](https://bitbucket.org/xi/pyyaml) if using the [facter plugin](https://github.com/tbielawa/jsonstats/blob/master/JsonStats/FetchStats/Plugins/Facter.py)


# Quick Start Guide

## Install It
Via *distutils*:

    sudo python ./setup.py install

Via *rpm* (requires development packages):

    make rpm
    sudo yum localinstall ./rpm-build/noarch/*.rpm

## Run It
Now we'll start `jsonstatsd` in a terminal. It won't detach from the
controlling shell. This means we'll have to `ctrl+c` the process when
we're done.

    /usr/bin/jsonstatsd
    Loading plugin... <class 'JsonStats.FetchStats.Fetcher'>
    Loading plugin... <class 'JsonStats.FetchStats.Plugins.RPM.RPM'>
    Loading plugin... <class 'JsonStats.FetchStats.Plugins.Facter.Facter'>
    Loading plugin... <class 'JsonStats.FetchStats.Plugins.DEB.DEB'>

Messages like *ERROR: Failed to load plugin 'foo'* aren't
critical. They just mean a required command wasn't found on our
system.

## Test It
In another terminal you can run a `curl` command like this to test
that the server is running*****:

    curl localhost:8008 | python -m json.tool

* *The* `python -m json.tool` *part is optional and is just there to reformat the output*

## Runtime Options
`jsonstatsd` can be configured at runtime with several other options:

    $ jsonstatsd --help
    Usage: jsonstatsd [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Port to listen on. (Default: 8008)
      -l LISTEN, --listen=LISTEN
                            Address to listen on. (Default: 0.0.0.0)
      --logdir=LOGDIR       Directory to log access requests to. (Default:
                            ./logs/)


# More Information

## Running As A System Service
To enable `jsonstatsd` as a system service on hosts still using the
`service` and `chkconfig` commands:

    sudo chkconfig jsonstatsd on
    sudo service jsonstatsd start

To enable `jsonstatsd` as a system service on `systemd` managed hosts:

    $ sudo systemctl enable jsonstatsd.service
    ln -s '/usr/lib/systemd/system/jsonstatsd.service' '/etc/systemd/system/multi-user.target.wants/jsonstatsd.service'


## Configuration
If you are running `jsonstatsd` as a system service (ex: via
`systemctl` or `service` commands) then you may want to examine the
service configuration file in `/etc/sysconfig/jsonstatsd`


    ######################################################################
    # Listen on all interfaces by default. You might also enjoy: 127.0.0.1
    # to just listen locally
    INTERFACE=0.0.0.0

    ######################################################################
    # Port to listen on
    PORT=8008

    ######################################################################
    # Customize the logging directory
    LOGDIR=/var/log/jsonstatsd

    ######################################################################
    # Single line with all options for the SysV init script
    OPTIONS="--listen $INTERFACE --port $PORT --logdir $LOGDIR"


## Logging
There are two log file which are produced by a running instance.

* **jsonstatsd_access.log**: Access log similar to apache's access log.
* **jsonstatsd.log**: Application level logging which logs some logic results.


## Tests
Run `make tests` to execute the test suite.


# Making new plugins
* New fact plugins MUST subclass the `Fetcher` parent class. Example:

        from JsonStats.FetchStats import Fetcher
        class MegaFrobber(Fetcher):

* Read the source for the `Fetcher` base class in
  `JsonStats/FetchStats/__init__.py` to see the remaining methods you
  must implement in your plugin.


* Until we come up with a better way of dynamically loading all
  plugins, new fact plugin module names MUST be added to the `__all__`
  list in `JsonStats/FetchStats/Plugins/__init__.py`
