======================================================
pyzmq-ctypes: Python bindings for 0MQ (ctypes version)
======================================================

This project is an attempt to build a partially-compatible version of
PyZMQ running on pypy. Since I don't have time to write a Cython that
compiles to Python instead of C, I decided to write some ctypes bindings
for ZeroMQ.

These bindings introspect parts of the ZeroMQ library by using the C
compiler and a C parser, so you will still need those in order to
use this.

Authors
=======

The ctypes bindings were written by Daniel Holth <dholth@gmail.com>
based on a copy of the original PyZMQ with the Cython bits taken out.

The orginal PyZMQ was started by and continues to be led by Brian
E. Granger (ellisonbg AT gmail DOT com).

The following people have contributed to the project:

* Carlos Rocha (carlos DOT rocha AT gmail DOT com)
* Andrew Gwozdziewycz (git AT apgwoz DOT com)
* Fernando Perez (fernando DOT perez AT berkeley DOT edu)
* Nicholas Piel (nicholas AT nichol DOT as)
* Eugene Chernyshov (chernyshov DOT eugene AT gmail DOT com)
* Justin Riley (justin DOT t DOT riley AT gmail DOT com)
* Ivo Danihelka (ivo AT denihelka DOT net)
* Thomas Supra (tomspur AT fedoraproject DOT org)
* Douglas Creager (dcreager AT dcreager DOT net)
* Erick Tryzelaar (erick DOT tryzelaar AT gmail DOT com)
* Min Ragan-Kelley (benjaminrk AT gmail DOT com)
* Scott Sadler (github AT mashi DOT org)
* spez (steve AT hipmunk DOT com)
* Thomas Kluyver (takowl AT gmail DOT com)
* Peter Ward (peteraward AT gmail DOT com)
