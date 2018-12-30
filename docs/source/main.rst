=======================================
RangeSet -- set of consecutive integers
=======================================

Rationale
---------

Python Sets are nice, but very inefficient if you need a large set with
mostly-consecutive integers.

Applications
============

RangeSet was written for `DistKV <https://github.com/smurfix/distkv>`,
a master-less distributed key-value store, to keep track of which changes
have been seen by which systems. These change indices grow without bound,
thus a regular set or a bitmap would not scale.

Usage
=====

A RangeSet works exactly like a Python set, with these exceptions:

* iterating a set yields a sequence of ``(start, end)`` tuples.
  The start value is part of the set while the end value is not.

* Likewise, initialization requires an iterator that yields ``(start,
  end)`` tuples. These tuples may overlap.

* You can add or remove single values as well as ``(start, end)`` tuples.

* There is no FrozenRangeSet class.

* You can only store integers.

* Worst-case behavior for inserting or removing a value is O(n).

* On the other hand, best-case behavior (for lists with no or few holes) is
  O(1) regardless of the size of the list.

* The length of a RangeSet is the number of distinct ranges. If you need
  the number of members, use the ``items`` method.


For usage, please refer to `the Python documentation
<https://docs.python.org/3.7/library/stdtypes.html#set-types-set-frozenset>`.

Non-integers?
=============

RangeSet works with anything that has discrete steps between values – IP
adresses come to mind. Just subclass ``RangeSet`` and change the ``_step``
method.

