import os
import sys

from distutils.core import Command, setup
from distutils.command.build_ext import build_ext
from traceback import print_exc

cython_available = False
try:
    from Cython.Distutils import build_ext
    from Cython.Distutils.extension import Extension
    cython_available = True
except ImportError, e:
    pass

try:
    import nose
except ImportError:
    nose = None

def get_ext_modules():
    if not cython_available:
        print 'WARNING: cython not available, proceeding with pure python implementation.'
        return []
    try:
        import meinheld
    except ImportError, e:
        print 'WARNING: meinheld must be installed to build cython version of meinheld-zeromq (%s).' % e
        return []
    try:
        import zmq
    except ImportError, e:
        print 'WARNING: pyzmq(==2.2.0) must be installed to build cython version of meinheld-zeromq (%s).' % e
        return []

    return [Extension('meinheld_zeromq.core', ['meinheld_zeromq/core.pyx'], include_dirs=zmq.get_includes())]

__version__ = (0, 0, 1)

setup(
    name = 'meinheld_zeromq',
    version = '.'.join([str(x) for x in __version__]),
    packages = ['meinheld_zeromq'],
    ext_modules = get_ext_modules(),
    author = 'INADA Naoki',
    author_email = 'songofacandy@gmail.com',
    url = 'http://github.com/methane/meinheld-zeromq',
    description = 'meinheld compatibility layer for pyzmq',
    long_description=open('README.rst').read(),
    install_requires = ['pyzmq==2.2.0', 'meinheld'],
    license = 'New BSD',
)
