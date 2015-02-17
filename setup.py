import os
import sys
import platform
from distutils.core import setup


# Technically platform.dist() was deprecated in 2.6, so lets play
# along and set a good example...
(py_major, py_minor, py_patch) = platform.python_version_tuple()

# Lets assume you're running python 2.x.y right now. We'll handle python 3 later
#if py_major == 2:
if int(py_minor) > 5:
    # Use the new hotness
    (distname, version, id) = platform.linux_distribution()
else:
    # Fall back
    (distname, version, id) = platform.dist()

# Determine which boot system we're targeting while building the RPM
#
# - RHEL5/6 uses SysV style scripts
# - RHEL7+/Fedora>=15 use systemd

boot_system = None
system_major = version.split('.')[0]
if distname.lower() == 'redhat' or 'Red Hat' in distname:
    if int(system_major) in [5, 6]:
        boot_system = 'sysv'
    elif int(system_major) >= 7:
        boot_system = 'systemd'
    else:
        # I don't even know how to deal with you right now
        boot_system = 'sysv'
elif distname.lower() == 'fedora':
    if int(system_major) >= 15:
        boot_system = 'systemd'
    else:
        boot_system = 'sysv'
else:
    # Too bad
    boot_system = 'sysv'

print boot_system

datum = {
    'systemd': ('/usr/lib/systemd/system', ['lib/systemd/system/jsonstatsd.service', ]),
    'sysv': ('/etc/rc.d/init.d', ['etc/rc.d/init.d/jsonstatsd', ]),
}

final_data_files = [
    ('/etc/sysconfig', ['etc/sysconfig/jsonstatsd', ]),
    datum[boot_system],
]


setup(name='jsonstats',
      version='1.0.4',
      description='Client for exposing system information over a REST interface',
      maintainer='Tim Bielawa',
      maintainer_email='tbielawa@redhat.com',
      url='https://github.com/RHInception/jsonstats',
      license='MIT',
      package_dir={'jsonstats': 'JsonStats'},
      packages=[
        'JsonStats',
        'JsonStats.FetchStats',
        'JsonStats.FetchStats.Plugins'
      ],
      scripts=[
        'bin/jsonstatsd',
      ],
      data_files=final_data_files,
)
