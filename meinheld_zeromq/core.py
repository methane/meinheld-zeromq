"""This module wraps the :class:`Socket` and :class:`Context` found in :mod:`pyzmq <zmq>` to be non blocking
"""
import zmq
from zmq import *
from zmq import devices
__all__ = zmq.__all__

from meinheld.server import trampoline


class GreenSocket(Socket):
    """Green version of :class:`zmq.core.socket.Socket`

    The following methods are overridden:

        * send
        * send_multipart
        * recv
        * recv_multipart

    To ensure that the ``zmq.NOBLOCK`` flag is set and that sending or recieving
    is deferred to the hub if a ``zmq.EAGAIN`` (retry) error is raised.
    
    Some double underscore prefixes are used to minimize pollution of
    :class:`zmq.core.socket.Socket`'s namespace.
    """

    def __init__(self, context, socket_type):
        self.__in_send_multipart = False
        self.__in_recv_multipart = False
        super(GreenSocket, self).__init__(context, socket_type)
        self._fd = self.getsockopt(zmq.FD)

    def _wait_write(self):
        trampoline(self._fd, False, True)

    def _wait_read(self):
        trampoline(self._fd, True, False)

    def send(self, data, flags=0, copy=True, track=False):
        # if we're given the NOBLOCK flag act as normal and let the EAGAIN get raised
        if flags & zmq.NOBLOCK:
            return super(GreenSocket, self).send(data, flags, copy, track)

        # ensure the zmq.NOBLOCK flag is part of flags
        flags |= zmq.NOBLOCK
        while True: # Attempt to complete this operation indefinitely, blocking the current greenlet
            try:
                # attempt the actual call
                return super(GreenSocket, self).send(data, flags, copy, track)
            except zmq.ZMQError, e:
                # if the raised ZMQError is not EAGAIN, reraise
                if e.errno != zmq.EAGAIN:
                    raise
                # defer to the event loop until we're notified the socket is writable
                self._wait_write()

    def recv(self, flags=0, copy=True, track=False):
        if flags & zmq.NOBLOCK:
            return super(GreenSocket, self).recv(flags, copy, track)

        flags |= zmq.NOBLOCK
        while True:
            try:
                return super(GreenSocket, self).recv(flags, copy, track)
            except zmq.ZMQError, e:
                if e.errno != zmq.EAGAIN:
                    raise
                self._wait_read()


class GreenContext(Context):
    """Replacement for :class:`zmq.core.context.Context`

    Ensures that the greened Socket above is used in calls to `socket`.
    """
    _socket_class = GreenSocket

