# -*- coding: utf-8 -*-
"""meinheld_zmq - meinheld compatibility with zeromq.

Usage
-----

Instead of importing zmq directly, do so in the following manner:

..

    from meinheld_zeromq import zmq


Any calls that would have blocked the current thread will now only block the
current green thread.

This compatibility is accomplished by ensuring the nonblocking flag is set
before any blocking operation and the ØMQ file descriptor is polled internally
to trigger needed events.
"""

from zmq import *
from zmq import devices
import meinheld_zeromq.core as zmq

zmq.Socket = zmq.GreenSocket
zmq.Context = zmq.GreenContext
Socket = zmq.GreenSocket
Context = zmq.GreenContext
#Poller = GreenPoller

def monkey_patch():
    """
    Monkey patches `zmq.Context` and `zmq.Socket`

    If test_suite is True, the pyzmq test suite will be patched for
    compatibility as well.
    """
    ozmq = __import__('zmq')
    ozmq.Socket = zmq.Socket
    ozmq.Context = zmq.Context

__all__ = zmq.__all__ + ['monkey_patch']
