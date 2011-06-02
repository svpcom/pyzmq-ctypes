#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright (c) 2010, 2011 Brian E. Granger
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import sys
import time

import zmq
from zmq.tests import BaseZMQTestCase
from zmq.utils.strtypes import bytes, unicode
try:
    from queue import Queue
except:
    from Queue import Queue

try:
    from nose import SkipTest
except ImportError:
    class SkipTest(Exception):
        pass

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------

class TestSocket(BaseZMQTestCase):

    def test_create(self):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        # Superluminal protocol not yet implemented
        self.assertRaisesErrno(zmq.EPROTONOSUPPORT, s.bind, 'ftl://a')
        self.assertRaisesErrno(zmq.EPROTONOSUPPORT, s.connect, 'ftl://a')
        self.assertRaisesErrno(zmq.EINVAL, s.bind, 'tcp://')
        s.close()
        del ctx
        
    def test_2_1_sockopts(self):
        "test non-uint64 sockopts introduced in zeromq 2.1.0"
        v = list(map(int, zmq.zmq_version().split('.', 2)[:2]))
        if not (v[0] >= 2 and v[1] >= 1):
            raise SkipTest
        p,s = self.create_bound_pair(zmq.PUB, zmq.SUB)
        p.setsockopt(zmq.LINGER, 0)
        self.assertEquals(p.getsockopt(zmq.LINGER), 0)
        p.setsockopt(zmq.LINGER, -1)
        self.assertEquals(p.getsockopt(zmq.LINGER), -1)
        self.assertEquals(p.getsockopt(zmq.HWM), 0)
        p.setsockopt(zmq.HWM, 11)
        self.assertEquals(p.getsockopt(zmq.HWM), 11)
        # p.setsockopt(zmq.EVENTS, zmq.POLLIN)
        self.assertEquals(p.getsockopt(zmq.EVENTS), zmq.POLLOUT)
        self.assertRaisesErrno(zmq.EINVAL, p.setsockopt,zmq.EVENTS, 2**7-1)
        self.assertEquals(p.getsockopt(zmq.TYPE), p.socket_type)
        self.assertEquals(p.getsockopt(zmq.TYPE), zmq.PUB)
        self.assertEquals(s.getsockopt(zmq.TYPE), s.socket_type)
        self.assertEquals(s.getsockopt(zmq.TYPE), zmq.SUB)
    
    def test_sockopt_roundtrip(self):
        "test set/getsockopt roundtrip."
        p = self.context.socket(zmq.PUB)
        self.assertEquals(p.getsockopt(zmq.HWM), 0)
        p.setsockopt(zmq.HWM, 11)
        self.assertEquals(p.getsockopt(zmq.HWM), 11)
                

    def test_close(self):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.close()
        self.assertRaises(zmq.ZMQError, s.bind, ''.encode())
        self.assertRaises(zmq.ZMQError, s.connect, ''.encode())
        self.assertRaises(zmq.ZMQError, s.setsockopt, zmq.SUBSCRIBE, ''.encode())
        self.assertRaises(zmq.ZMQError, s.send, 'asdf'.encode())
        self.assertRaises(zmq.ZMQError, s.recv)
        del ctx
    

