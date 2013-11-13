import os
import sys

from distutils.core import setup

setup(name='jsonstats',
      version='0.5.0',
      description='Client for exposing system information over a REST interface',
      maintainer='Tim Bielawa',
      maintainer_email='tbielawa@redhat.com',
      url='https://github.com/tbielawa/restfulstatsjson',
      license='MIT',
      package_dir={ 'jsonstats': 'JsonStats' },
      packages=[
        'JsonStats',
        'JsonStats.FetchStats',
        'JsonStats.FetchStats.Plugins'
        ],
      scripts=[
        'bin/jsonstats',
        ],
)
