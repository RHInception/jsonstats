# jsonstats
[![Build Status](https://travis-ci.org/RHInception/jsonstats.png?branch=devel)](https://travis-ci.org/RHInception/jsonstats)

RESTful backend service for querying arbitraty system "facts".

## Features
* Minimal set of requirements
* Python 2.4+ compatible
* Access and application logging
* host and environment REST endpoints
* Unit tested

### Plugins
The following plugins come stock with jsonstats:

* Deb - Lists installed debian/ubuntu packages
* Facter - Lists system information from the facter command
* Pip - Lists installed pip packages
* RPM - Lists installed rpm packages
* Timestamp - Timestamp of when the data was requested

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

### RHEL Machines
On RHEL machines you will need the **EPEL** repositories installed for
the PyYAML package.

**RHEL6**:

    sudo rpm -Uvh http://mirror.pnl.gov/epel/6/i386/epel-release-6-8.noarch.rpm

**RHEL5**:

    sudo rpm -Uvh http://mirror.chpc.utah.edu/pub/epel/5/i386/epel-release-5-4.noarch.rpm


## Run It
Now we'll start `jsonstatsd` in a terminal. It won't detach from our
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
In another terminal we can run a `curl` command like this to test
that the server is running:

    curl localhost:8008 | python -m json.tool

* *The* `python -m json.tool` *part is optional and is just there to reformat the output*

Depending on which plugins loaded, we should see output similar to the
following:

```json
{
    "facter": {
        "architecture": "x86_64",
        "augeasversion": "1.0.0",
        "facterversion": "1.6.18",
        "hardwareisa": "x86_64",
        "hardwaremodel": "x86_64",
        "id": "jsonstatsd",
        "interfaces": "em1,lo,tun0,wlan0",
        "ipaddress": "::1",
        "is_virtual": "false",
        "kernel": "Linux",
        "kernelmajversion": "3.9",
        "kernelrelease": "3.9.10-100.fc17.x86_64",
        "kernelversion": "3.9.10",
        "lsbdistcodename": "BeefyMiracle",
        "lsbdistdescription": "Fedora release 17 (Beefy Miracle)",
        "lsbdistid": "Fedora"
    },
    "rpm": {
        "AdobeReader_enu": "9.5.1",
        "GConf2": "3.2.5",
        "GeoIP": "1.4.8",
        "GitPython": "0.3.2",
        "GraphicsMagick": "1.3.17",
        "GraphicsMagick-c++": "1.3.17",
        "HandBrake-cli": "0.9.8",
        "HandBrake-gui": "0.9.8",
        "ImageMagick": "6.7.5.6",
        "ImageMagick-c++": "6.7.5.6",
        "ImageMagick-perl": "6.7.5.6",
        "LibRaw": "0.14.8",
        "ModemManager": "0.6.2.0",
        "NetworkManager": "0.9.6.4",
        "NetworkManager-glib": "0.9.6.4",
        "NetworkManager-gnome": "0.9.6.4",
        "NetworkManager-gtk": "0.9.6.4",
        "NetworkManager-openconnect": "0.9.4.0",
        "NetworkManager-openvpn": "0.9.3.997",
        "jsonstatsd": "1.0.0"
    }
}
```

On my example system the
[Facter](http://puppetlabs.com/blog/facter-part-1-facter-101) and
[RPM](http://www.rpm.org/) plugins loaded. In the first block
(following **"facter": {**) we can see the key names are `facter` facts,
as reported by the `/usr/bin/facter` command. In the second block
(following **"rpm": {**) we receive a manifest of the name and version
of all RPM packages installed on the system.


## Runtime Options
`jsonstatsd` can be configured at runtime with several other options:

    $ jsonstatsd --help
    Usage: jsonstatsd [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Port to listen on (Default: 8008)
      -l LISTEN, --listen=LISTEN
                            Address to listen on (Default: 0.0.0.0)
      --logdir=LOGDIR       Directory to log access requests to (Default:
                            ./logs/)
      -e PLUGIN_PATHSPEC --extra-plugins=PLUGIN_PATHSPEC
                            Path to directory with additional plugins


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
    # See 'man 1 jsonstatsd' or 'jsonstatsd --help' for descriptions of
    # all the available options
    ######################################################################

    OPTIONS="--listen 0.0.0.0 --port 8008 --logdir /var/log/jsonstatsd"


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

* Plugins MUST return a Dictionary (hash) type data structure.

* Until we come up with a better way of dynamically loading all
  plugins, new fact plugin module names MUST be added to the `__all__`
  list in `JsonStats/FetchStats/Plugins/__init__.py`

*This issue is being tracked in [rfe: configurable 'extra plugins' parameter](https://github.com/RHInception/jsonstats/issues/2)*

## Building the Man Pages
Building the man pages requires the `a2x` command. This is usually
provided by the `asciidoc` package.

If `make docs` says:

    make: Nothing to be done for `docs'.

Then you should just need to do this:

    $ touch VERSION; make docs
