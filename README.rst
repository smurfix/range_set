ConSet
======

License: Your choice of MIT or Apache License 2.0

---------

Python Sets are nice to work with, but very inefficient if you need a large
set with mostly-consecutive integers. The ConSet class provides efficient
handling and storage for these sets.

Non-integers?
=============

ConSet works with any class whose instances are

* comparable

* step-able, i.e. you can add 1 to them / subtract 1 from them.

* discrete, i.e. there is no value between ``n`` and ``n+1``.

ConSet doesn't add or subtract any other values, nor does it try to
subtract two instances from each other.

The requirement to subtract 1 is an optimization that could be removed if
necessary.

