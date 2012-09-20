# -*- coding: utf-8 -*-
"""
Low-level ctypes binding for the ZeroMQ library.

Makes an attempt to emulate pyzmq.core.
"""
# Copyright © 2011 Daniel Holth
# 
# Derived from original pyzmq © 2010 Brian Granger
#
# This file is part of pyzmq-ctypes
#
# pyzmq-ctypes is free software; you can redistribute it and/or modify it
# under the terms of the Lesser GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pyzmq-ctypes is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU General Public
# License for more details.
#
# You should have received a copy of the Lesser GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import random

from ctypes import *
from ctypes.util import find_library
from ctypes_configure import configure

class CConfigure(object):
    _compilation_info_ = configure.ExternalCompilationInfo(
            includes = ['zmq.h'],
            libraries = ['zmq']
            )
    size_t = configure.SimpleType('size_t', c_long)
    
for cname in ['ZMQ_AFFINITY', 'ZMQ_DOWNSTREAM', 'EADDRINUSE',
    'EADDRNOTAVAIL', 'EAGAIN', 'ECONNREFUSED', 'EFAULT', 'EFSM',
    'EINPROGRESS', 'EINVAL', 'EMTHREAD', 'ENETDOWN', 'ENOBUFS',
    'ENOCOMPATPROTO', 'ENODEV', 'ENOMEM', 'ENOTSUP', 'EPROTONOSUPPORT',
    'ETERM', 'ZMQ_FORWARDER', 'ZMQ_HWM', 'ZMQ_IDENTITY', 'ZMQ_MCAST_LOOP',
    'ZMQ_NOBLOCK', 'ZMQ_PAIR', 'ZMQ_POLLERR', 'ZMQ_POLLIN', 'ZMQ_POLLOUT',
    'ZMQ_PUB', 'ZMQ_PULL', 'ZMQ_PUSH', 'ZMQ_QUEUE', 'ZMQ_RATE', 'ZMQ_RCVBUF',
    'ZMQ_RCVMORE', 'ZMQ_RECOVERY_IVL', 'ZMQ_REP', 'ZMQ_REQ', 'ZMQ_SNDBUF',
    'ZMQ_SNDMORE', 'ZMQ_STREAMER', 'ZMQ_SUB', 'ZMQ_SUBSCRIBE', 'ZMQ_SWAP',
    'ZMQ_UNSUBSCRIBE', 'ZMQ_UPSTREAM', 'ZMQ_XREP', 'ZMQ_XREQ', 'ZMQ_MAX_VSM_SIZE',
    'ZMQ_FD', 'ZMQ_EVENTS', 'ZMQ_TYPE', 'ZMQ_LINGER', 'ZMQ_RECONNECT_IVL',
    'ZMQ_BACKLOG', 'ZMQ_DEALER', 'ZMQ_ROUTER']:
        pyname = cname.split('_', 1)[-1]
        setattr(CConfigure, pyname, configure.ConstantInteger(cname))

info = configure.configure(CConfigure)
globals().update(info)

# collections of sockopts, based on type:
bytes_sockopts = [SUBSCRIBE, UNSUBSCRIBE, IDENTITY]
int64_sockopts = [HWM, SWAP, AFFINITY, RATE, RECOVERY_IVL,
                MCAST_LOOP, SNDBUF, RCVBUF, RCVMORE]
int_sockopts = [FD, EVENTS, TYPE, LINGER, RECONNECT_IVL, BACKLOG]

class ZMQBaseError(Exception): pass

class ZMQError(ZMQBaseError):
    def __init__(self, errno=None):
        if errno is None:
            errno = get_errno()
        self.strerror = zmq_strerror(errno)
        self.errno = errno

    def __str__(self):
        return self.strerror  

def _check_nonzero(result, func, arguments):
    if result == -1:
        raise ZMQError(get_errno())
    return result

def _check_not_null(result, func, arguments):
    if result is None:
        raise ZMQError(get_errno())
    return result

def _check_zmq_errno(result, func, arguments):
    errno = get_errno()
    if errno != 0:
        raise ZMQError(errno)
    return result

libzmq = CDLL(find_library("zmq"), use_errno=True)

libzmq.zmq_version.restype = None
libzmq.zmq_version.argtypes = [POINTER(c_int)]*3

major = c_int()
minor = c_int()
patch = c_int()

libzmq.zmq_version(byref(major), byref(minor), byref(patch))

__zmq_version__ = tuple((x.value for x in (major, minor, patch)))

def zmq_version():
    return '.'.join(map(str, __zmq_version__))

memmove.restype = c_void_p
# Error number as known by the 0MQ library

libzmq.zmq_errno.argtypes = []

libzmq.zmq_strerror.restype = c_char_p
libzmq.zmq_strerror.argtypes = [c_int]

# 0MQ infrastructure

libzmq.zmq_init.restype = c_void_p
libzmq.zmq_init.argtypes = [c_int]

libzmq.zmq_term.restype = c_int # the default
libzmq.zmq_term.argtypes = [c_void_p]

# 0MQ message definition

class zmq_msg_t(Structure):
    _fields_ = [
            ('content', c_void_p),
            ('flags', c_ubyte),
            ('vsm_size', c_ubyte),
            ('vsm_data', c_ubyte*MAX_VSM_SIZE)
            ]

libzmq.zmq_msg_init.argtypes = [POINTER(zmq_msg_t)]
libzmq.zmq_msg_init.restype = c_int
libzmq.zmq_msg_init_size.restype = c_int
libzmq.zmq_msg_init_size.argtypes = [POINTER(zmq_msg_t), size_t]

# requires a free function:
libzmq.zmq_msg_init_data.restype = c_int
libzmq.zmq_msg_init_data.argtypes = [POINTER(zmq_msg_t), c_void_p, size_t,
                                     c_void_p, c_void_p]
libzmq.zmq_msg_close.restype = c_int
libzmq.zmq_msg_close.argtypes = [POINTER(zmq_msg_t)]
libzmq.zmq_msg_move.argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)]
libzmq.zmq_msg_copy.argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)]
libzmq.zmq_msg_data.restype = c_void_p
libzmq.zmq_msg_data.argtypes = [POINTER(zmq_msg_t)]
libzmq.zmq_msg_size.restype = size_t
libzmq.zmq_msg_size.argtypes = [POINTER(zmq_msg_t)]

# 0MQ socket definition

libzmq.zmq_socket.restype = c_void_p
libzmq.zmq_socket.argtypes = [c_void_p, c_int]
libzmq.zmq_socket.errcheck = _check_not_null

libzmq.zmq_close.restype = c_int
libzmq.zmq_close.argtypes = [c_void_p]

libzmq.zmq_setsockopt.restype = c_int
libzmq.zmq_setsockopt.argtypes = [c_void_p, c_int, c_void_p, size_t]
libzmq.zmq_getsockopt.restype = c_int
libzmq.zmq_getsockopt.argtypes = [c_void_p, c_int, c_void_p, POINTER(size_t)]
libzmq.zmq_bind.restype = c_int
libzmq.zmq_bind.argtypes = [c_void_p, c_char_p]
libzmq.zmq_connect.restype = c_int
libzmq.zmq_connect.argtypes = [c_void_p, c_char_p]
libzmq.zmq_send.restype = c_int
libzmq.zmq_send.argtypes = [c_void_p, POINTER(zmq_msg_t), c_int]
libzmq.zmq_recv.restype = c_int
libzmq.zmq_recv.argtypes = [c_void_p, POINTER(zmq_msg_t), c_int]

class zmq_pollitem_t(Structure):
    _fields_ = [
            ('socket', c_void_p),
            ('fd', c_int),
            ('events', c_short),
            ('revents', c_short)
            ]

libzmq.zmq_poll.restype = c_int
libzmq.zmq_poll.argtypes = [POINTER(zmq_pollitem_t), c_int, c_long]

def _default_errcheck():
    for symbol in dir(libzmq):
        if symbol.startswith('zmq_'):
            fn = getattr(libzmq, symbol)
            if fn.errcheck != None:
                continue
            if fn.restype is c_int:
                fn.errcheck = _check_nonzero
            elif fn.restype is c_void_p:
                fn.errcheck = _check_not_null
            
def _shortcuts():       
    for symbol in dir(libzmq):
        if symbol.startswith('zmq_') and not symbol in globals():
            fn = getattr(libzmq, symbol)  
            globals()[symbol] = fn     

_default_errcheck()
_shortcuts()

# Higher-level interface. Partially copied from pyzmq.

class Context(object):
    def __init__(self, io_threads=1):
        """The io_threads argument specifies the size of the ØMQ thread pool to
        handle I/O operations. If your application is using only the inproc 
        transport for messaging you may set this to zero, otherwise set it to 
        at least one."""
        if not io_threads > 0:
            raise ZMQError(EINVAL)
        self.handle = zmq_init(io_threads)
        self.closed = False
        
    def socket(self, kind):
        if self.closed:
            raise ZMQError(ENOTSUP)
        return Socket(self, kind)
    
    def term(self):
        rc = zmq_term(self.handle)
        self.handle = None
        self.closed = True
        return rc
    
class Socket(object):
    def __init__(self, context, socket_type):
        self.context = context
        self.handle = zmq_socket(context.handle, socket_type)
        self.socket_type = socket_type
        self.closed = False
    
    def _check_closed(self):
        if self.closed:
            raise ZMQError(ENOTSUP)
        
    def close(self):
        zmq_close(self.handle)
        self.handle = None
        self.closed = True
        
    def bind(self, addr):
        if isinstance(addr, unicode):
            addr = addr.encode('utf-8')
        if not isinstance(addr, bytes):
            raise TypeError('expected str, got: %r' % addr)
        zmq_bind(self.handle, addr)
        
    def bind_to_random_port(self, addr, min_port=2000, max_port=20000, max_tries=100):
        """s.bind_to_random_port(addr, min_port=2000, max_port=20000, max_tries=100)

        Bind this socket to a random port in a range.

        Parameters
        ----------
        addr : str
            The address string without the port to pass to ``Socket.bind()``.
        min_port : int, optional
            The minimum port in the range of ports to try.
        max_port : int, optional
            The maximum port in the range of ports to try.
        max_tries : int, optional
            The number of attempt to bind.

        Returns
        -------
        port : int
            The port the socket was bound to.
        
        Raises
        ------
        ZMQBindError
            if `max_tries` reached before successful bind
        """
        for i in range(max_tries):
            try:
                port = random.randrange(min_port, max_port)
                self.bind('%s:%s' % (addr, port))
            except ZMQError:
                pass
            else:
                return port
        raise ZMQBindError("Could not bind socket to random port.")
    
    def connect(self, addr):
        """s.connect(addr)

        Connect to a remote 0MQ socket.

        Parameters
        ----------
        addr : str
            The address string. This has the form 'protocol://interface:port',
            for example 'tcp://127.0.0.1:5555'. Protocols supported are
            tcp, upd, pgm, inproc and ipc. If the address is unicode, it is
            encoded to utf-8 first.
        """
        if isinstance(addr, unicode):
            addr = addr.encode('utf-8')
        if not isinstance(addr, bytes):
            raise TypeError('expected str, got: %r' % addr)
        zmq_connect(self.handle, addr)

    @property
    def rcvmore(self):
        """s.rcvmore()

        Are there more parts to a multipart message?
        
        Returns
        -------
        more : bool
            whether we are in the middle of a multipart message.
        """
        more = self.getsockopt(RCVMORE)
        return bool(more)


    def getsockopt(self, option):
        """s.getsockopt(option)

        Get the value of a socket option.

        See the 0MQ documentation for details on specific options.

        Parameters
        ----------
        option : str
            The name of the option to set. Can be any of: 
            IDENTITY, HWM, SWAP, AFFINITY, RATE, 
            RECOVERY_IVL, MCAST_LOOP, SNDBUF, RCVBUF, RCVMORE.

        Returns
        -------
        optval : int, str
            The value of the option as a string or int.
        """

        self._check_closed()

        optval = 0

        if option in int64_sockopts:
            optval = c_int64(optval)
        elif option in int_sockopts:
            optval = c_int32(optval)
        else:
            raise ZMQError(EINVAL)

        optlen = size_t(sizeof(optval))
        zmq_getsockopt(self.handle, option, byref(optval), byref(optlen))
        return optval.value

        
    def setsockopt(self, option, optval):
        """s.setsockopt(option, optval)

        Set socket options.

        See the 0MQ documentation for details on specific options.

        Parameters
        ----------
        option : constant
            The name of the option to set. Can be any of: SUBSCRIBE, 
            UNSUBSCRIBE, IDENTITY, HWM, SWAP, AFFINITY, RATE, 
            RECOVERY_IVL, MCAST_LOOP, SNDBUF, RCVBUF.
        optval : int or str
            The value of the option to set.
        """

        self._check_closed()
        if isinstance(optval, unicode):
            raise TypeError("unicode not allowed, use setsockopt_unicode")

        if option in bytes_sockopts:
            if not isinstance(optval, bytes):
                raise TypeError('expected str, got: %r' % optval)
            zmq_setsockopt(self.handle, option, optval, len(optval))
        elif option in int64_sockopts:
            if not isinstance(optval, int):
                raise TypeError('expected int, got: %r' % optval)
            optval_int64_c = c_int64(optval)
            zmq_setsockopt(self.handle, option,
                    byref(optval_int64_c), sizeof(optval_int64_c))
        elif option in int_sockopts:
            if not isinstance(optval, int):
                raise TypeError('expected int, got: %r' % optval)
            optval_int32_c = c_int32(optval)
            zmq_setsockopt(self.handle, option,
                    byref(optval_int32_c), sizeof(optval_int32_c))

        else:
            raise ZMQError(EINVAL)


    def send(self, data, flags=0, copy=True, track=False):
        """s.send(data, flags=0, copy=True, track=False)

        Send a message on this socket.

        This queues the message to be sent by the IO thread at a later time.

        Parameters
        ----------
        data : object, str, Message
            The content of the message.
        flags : int
            Any supported flag: NOBLOCK, SNDMORE.
        copy : bool
            Should the message be sent in a copying or non-copying manner.
        track : bool
            Should the message be tracked for notification that ZMQ has
            finished with it? (ignored if copy=True)

        Returns
        -------
        None : if `copy` or not track
            None if message was sent, raises an exception otherwise.
        MessageTracker : if track and not copy
            a MessageTracker object, whose `pending` property will
            be True until the send is completed.
        
        Raises
        ------
        TypeError
            If a unicode object is passed
        ValueError
            If `track=True`, but an untracked Message is passed.
        ZMQError
            If the send does not succeed for any reason.
        
        """
        self._check_closed()
        
        if isinstance(data, unicode):
            raise TypeError("unicode not allowed, use send_unicode")

        if not isinstance(data, bytes):
                raise TypeError('expected str, got: %r' % data)
        
        flags = c_int(flags)

        msg = zmq_msg_t()
        msg_c_len = len(data)

        zmq_msg_init_size(byref(msg), msg_c_len)
        msg_buf = zmq_msg_data(byref(msg))
        msg_buf_size = zmq_msg_size(byref(msg))
        memmove(msg_buf, data, msg_buf_size)

        return zmq_send(self.handle, byref(msg), flags)
            

    def recv(self, flags=0, copy=True, track=False):
        """s.recv(flags=0, copy=True, track=False)

        Receive a message.

        Parameters
        ----------
        flags : int
            Any supported flag: NOBLOCK. If NOBLOCK is set, this method
            will raise a ZMQError with EAGAIN if a message is not ready.
            If NOBLOCK is not set, then this method will block until a
            message arrives.
        copy : bool
            Should the message be received in a copying or non-copying manner?
            If False a Message object is returned, if True a string copy of
            message is returned.
        track : bool
            Should the message be tracked for notification that ZMQ has
            finished with it? (ignored if copy=True)

        Returns
        -------
        msg : str, Message
            The returned message.  If `copy` is False, then it will be a Message,
            otherwise a str.
            
        Raises
        ------
        ZMQError
            for any of the reasons zmq_recvmsg might fail.
        """

        self._check_closed()

        flags = c_int(flags)
        msg = zmq_msg_t()

        zmq_msg_init(byref(msg))
        try:
            zmq_recv(self.handle, byref(msg), flags)
            data = zmq_msg_data(byref(msg))
            data_size = zmq_msg_size(byref(msg))
            return string_at(data, data_size)
        finally:
            zmq_msg_close(byref(msg))

def _poll(sockets, timeout=-1):
    """_poll(sockets, timeout=-1)

    Poll a set of 0MQ sockets, native file descs. or sockets.

    Parameters
    ----------
    sockets : list of tuples of (socket, flags)
        Each element of this list is a two-tuple containing a socket
        and a flags. The socket may be a 0MQ socket or any object with
        a ``fileno()`` method. The flags can be zmq.POLLIN (for detecting
        for incoming messages), zmq.POLLOUT (for detecting that send is OK)
        or zmq.POLLIN|zmq.POLLOUT for detecting both.
    timeout : int
        The number of milliseconds to poll for. Negative means no timeout.
    """
    if major < c_int(3):
        # timeout is us in 2.x, ms in 3.x
        # expected input is ms (matches 3.x)
        timeout = 1000 * timeout

    n_sockets = len(sockets)

    array_type = zmq_pollitem_t * n_sockets
    pollitems = array_type()

    for i, (s, events) in enumerate(sockets):
        if isinstance(s, Socket):
            pollitems[i].socket = s.handle
            pollitems[i].events = events
            pollitems[i].revents = 0
        elif isinstance(s, int_t):
            pollitems[i].socket = NULL
            pollitems[i].fd = s
            pollitems[i].events = events
            pollitems[i].revents = 0
        elif hasattr(s, 'fileno'):
            try:
                fileno = int(s.fileno())
            except:
                raise ValueError('fileno() must return an valid integer fd')
            else:
                pollitems[i].socket = NULL
                pollitems[i].fd = fileno
                pollitems[i].events = events
                pollitems[i].revents = 0
        else:
            raise TypeError(
                "Socket must be a 0MQ socket, an integer fd or have "
                "a fileno() method: %r" % s
            )

    zmq_poll(pollitems, n_sockets, timeout)

    results = []
    for i, (s, _) in enumerate(sockets):
        # Return the fd for sockets, for compat. with select.poll.
        if hasattr(s, 'fileno'):
            s = s.fileno()
        revents = pollitems[i].revents
        # Only return sockets with non-zero status for compat. with select.poll.
        if revents > 0:
            results.append((s, revents))

    return results

class Poller(object):
    """Poller()

    A stateful poll interface that mirrors Python's built-in poll.
    """

    def __init__(self):
        self.sockets = {}

    def register(self, socket, flags=POLLIN|POLLOUT):
        """p.register(socket, flags=POLLIN|POLLOUT)

        Register a 0MQ socket or native fd for I/O monitoring.

        register(s,0) is equivalent to unregister(s).

        Parameters
        ----------
        socket : zmq.Socket or native socket
            A zmq.Socket or any Python object having a ``fileno()``
            method that returns a valid file descriptor.
        flags : int
            The events to watch for.  Can be POLLIN, POLLOUT or POLLIN|POLLOUT.
            If `flags=0`, socket will be unregistered.
        """
        if flags:
            self.sockets[socket] = flags
        elif socket in self.sockets:
            # uregister sockets registered with no events
            self.unregister(socket)
        else:
            # ignore new sockets with no events
            pass

    def modify(self, socket, flags=POLLIN|POLLOUT):
        """p.modify(socket, flags=POLLIN|POLLOUT)

        Modify the flags for an already registered 0MQ socket or native fd.
        """
        self.register(socket, flags)

    def unregister(self, socket):
        """p.unregister(socket)

        Remove a 0MQ socket or native fd for I/O monitoring.

        Parameters
        ----------
        socket : Socket
            The socket instance to stop polling.
        """
        del self.sockets[socket]

    def poll(self, timeout=None):
        """p.poll(timeout=None)

        Poll the registered 0MQ or native fds for I/O.

        Parameters
        ----------
        timeout : float, int
            The timeout in milliseconds. If None, no `timeout` (infinite). This
            is in milliseconds to be compatible with ``select.poll()``. The
            underlying zmq_poll uses microseconds and we convert to that in
            this function.
        """
        if timeout is None:
            timeout = -1

        timeout = int(timeout)
        if timeout < 0:
            timeout = -1
        return _poll(list(self.sockets.items()), timeout=timeout)

