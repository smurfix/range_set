"""Top-level package for RangeSet."""

from importlib.metadata import version  # part of setuptools

_version = version("range_set")
del version

_version_tuple = tuple(int(x) for x in _version.split("."))




class RangeSet:
    """
    A RangeSet works exactly like a Python set, with these exceptions:

    * iterating a set yields a sequence of ``(start, end)`` tuples.
      The start value is part of the set while the end value is not.

    * You can add or remove single values as well as ``(start, end)`` tuples.

    * Likewise, initialization works with an iterator that yields single
      values or ``(start, end)`` tuples. These tuples may overlap.

    * There is no FrozenRangeSet class.

    * You can only store integers.

    * Worst-case behavior for inserting or removing a value is O(n).

    * On the other hand, best-case behavior (for lists with no or few holes) is
      O(1) regardless of the size of the list.
    """

    def __init__(self, iter=None):
        self._set = []
        if iter is not None:
            for x in iter:
                if isinstance(x, tuple):
                    self.add(*x)
                else:
                    self.add(x)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._set))

    def __getstate__(self):
        def state():
            for x, y in self._set:
                if x + 1 == y:
                    yield x
                else:
                    yield (x, y)

        return list(state())

    def __setstate__(self, state):
        self._set = s = []
        for x in state:
            if isinstance(x, list):
                assert len(x) == 2
                s.append((x[0], x[1]))
            elif isinstance(x, tuple):
                assert len(x) == 2
                s.append(x)
            else:
                s.append((x, x + 1))

    def _find(self, x):
        """Return the position of x within the array.
        (n, False) means that x is after position n.
        (n, True) means that x is within position n.
        n==-1 means before the beginning of the array.

        This method cannot be called with empty lists.

        ``add`` and ``remove`` call this method with the element shifted
        away from the range's edge, i.e. they behave as if the element just
        on the boundary of an interval is not actually part of that
        interval. This simplifies their algorithm considerably.
        """
        s = self._set
        lo = 0
        hi = len(s)
        if x >= s[-1][1]:
            return (hi - 1, False)
        if x >= s[-1][0]:
            return (hi - 1, True)
        if x < s[0][0]:
            return (-1, False)
        if x < s[0][1]:
            return (0, True)

        while lo < hi:
            mid = (lo + hi) // 2
            if x >= s[mid][0] and x < s[mid][1]:
                return (mid, True)
            elif x < s[mid][0]:
                hi = mid
            else:
                lo = mid + 1
        return (lo - 1, False)

    def __iter__(self):
        return self._set.__iter__()

    def copy(self):
        """Return a new set with a shallow copy of s."""
        s = RangeSet()
        s._set = self._set[:]
        return s

    def add(self, x, y=None):
        """Add an item (or a range of items) to the set.

        Arguments:
          ``x``: the first (or only) item to be added.
          ``y``: one item past the range that should not be added.
        """
        if y is None:
            y = x + 1
        s = self._set
        l = len(s)

        if l == 0:
            s.append((x, y))
            return

        (p, pi) = self._find(x - 1)
        (q, qi) = self._find(y)
        if p == l - 1 and not pi:
            s.append((x, y))
            return
        if not pi and not qi and p == q:
            s.insert(p + 1, (x, y))
            return
        if pi:
            x = min(x, s[p][0])
        if qi:
            y = max(y, s[q][1])

        if not pi:
            p += 1
        del s[p:q]
        s[p] = (x, y)

    def pop(self):
        """Remove an arbitrary item.

        We keep it simple and always remove the last one.
        """
        s = self._set
        if not s:
            raise KeyError()
        x = s[-1][1] - 1
        self.remove(x)
        return x

    def discard(self, x, y=None):
        """
        Like ``remove`` but does not raise an error if the item (or range)
        is not present.
        """
        self.remove(x, y, error=False)

    def present(self, x, y):
        """Check if the range [x…y) is contained in the set."""
        if not self._set:
            return False
        p, pi = self._find(x)
        q, qi = self._find(y - 1)
        return pi and qi and p == q

    def absent(self, x, y):
        """Check if no item in the range [x…y) is contained in the set."""
        if not self._set:
            return False
        p, pi = self._find(x)
        if pi:
            return False
        q, qi = self._find(y - 1)
        if qi:
            return False
        return p == q

    def remove(self, x, y=None, error=True):
        """Remove an item (or a range of items) from the set.

        Arguments:
          ``x``: the first (or only) item to be removed.
          ``y``: one item past the range that should not be removed.
          ``error``: if set (the default), raise KeyError if no element has been removed.

        """
        s = self._set
        l = len(s)
        if l == 0:
            if error:
                raise KeyError((x, y))
            return
        if y is None:
            y = x + 1

        (p, pi) = self._find(x - 1)
        if p == l - 1 and not pi:
            if error:
                raise KeyError((x, y))
            return

        (q, qi) = self._find(y)
        if not pi and not qi and p == q:
            # This includes q<0
            if error:
                raise KeyError((x, y))
            return
        if pi and qi and p == q:
            # Removing from inside a range: split it.
            s.insert(p, (s[p][0], x))
            s[p + 1] = (y, s[p + 1][1])
            return
        if pi:
            s[p] = (s[p][0], x)
            # the start is always kept because if it would be
            # deleted, p is the previous index and pi is False
        if qi:
            s[q] = (y, s[q][1])
        else:  # don't keep the end
            q += 1
        del s[p + 1:q]

    def __contains__(self, x):
        if not self._set:
            return False
        _, f = self._find(x)
        return f

    def __len__(self):
        return len(self._set)

    def count(self):
        """Count the total number of elemnts in the set.
        In contrast, ``len()`` counts the number of distinct ranges.
        """
        n = 0
        for a, b in self._set:
            n += b - a
        return n

    def isdisjoint(self, other):
        """Return ``True`` if the set has no elements in common with other.

        Sets are disjoint if and only if their intersection is the empty set.
        """
        a = iter(self)
        b = iter(other)

        try:
            ax, ay = next(a)
            bx, by = next(b)
            while True:
                if ax >= by:
                    bx, by = next(b)
                elif bx >= ay:
                    ax, ay = next(a)
                else:
                    return False
        except StopIteration:
            return True

    def issubset(self, other, proper=False):
        """Check whether every element in the set is in other.

        Args:
          ``other``: The set this should be a subset of.
          ``proper``: If set, return ``False`` if the sets are identical.
        """
        a = iter(self)
        b = iter(other)
        disjoint = False

        try:
            ax, ay = next(a)
        except StopIteration:
            try:
                next(b)
            except StopIteration:
                return True
            else:
                return not proper
        try:
            bx, by = next(b)
        except StopIteration:
            return False

        while True:
            while ax >= by:
                try:
                    bx, by = next(b)
                except StopIteration:
                    return False
            if proper and (ax != bx or ay != by):
                disjoint = True

            if ax < bx:
                return False
            if ay > by:
                return False
            try:
                ax, ay = next(a)
            except StopIteration:
                return disjoint or not proper

    def __lt__(self, other):
        return self.issubset(other, True)

    def __le__(self, other):
        return self.issubset(other, False)

    def issuperset(self, other, proper=False):
        """Test if every element of the other set is in this one.

        Args:
          ``other``: The set this should be a subset of.
          ``proper``: If set, return ``False`` if the sets are identical.
        """
        return other.issubset(self, proper=proper)

    def __eq__(self, other):
        return self._set == other._set

    def __gt__(self, other):
        return other.issubset(self, True)

    def __ge__(self, other):
        return other.issubset(self, False)

    def span(self):
        """Returns the smallest RangeSet encapsulating all items in this set"""
        s = self._set
        r = RangeSet()
        if s:
            r._set.append((s[0][0], s[-1][1]))
        return r

    # TODO:
    # all of the following methods are somewhat inefficient and should be
    # replaced with direct implementations.

    def update(self, *others):
        """Update the set, adding elements from all others."""
        for o in others:
            self |= o
        return self

    __iadd__ = update

    def union(self, *others):
        """Return a new set with elements from the set and all others."""
        s = self.copy()
        s.update(*others)
        return s

    __add__ = union

    union_update = update

    def __or__(self, other):
        s = self.copy()
        s |= other
        return s

    def intersection(self, *others):
        """Return a new set with elements common to the set and all others."""
        s = self.copy()
        s.intersection_update(*others)
        return s

    def intersection_update(self, *others):
        """Update the set, keeping only elements found in it and all others."""
        for o in others:
            self &= o
        return self

    def __and__(self, other):
        s = self.copy()
        s &= other
        return s

    def __ior__(self, other):
        for x, y in other:
            self.add(x, y)
        return self

    def __iand__(self, other):
        # TODO: this is particularly bad
        s = self ^ other
        self -= s
        return self

    def difference(self, *others):
        """Return a new set with elements in the set that are not in the others."""
        s = self.copy()
        s.difference_update(*others)
        return s

    def difference_update(self, *others):
        """Update the set, removing elements found in others."""
        for o in others:
            self -= o
        return self

    def __sub__(self, other):
        s = self.copy()
        s -= other
        return s

    def __isub__(self, other):
        for x, y in other:
            self.discard(x, y)
        return self

    def __ixor__(self, other):
        s = other - self
        self -= other
        self |= s
        return self

    def symmetric_difference(self, *others):
        """Return a new set with elements in either this set or ``other`` but not both."""
        s = self.copy()
        s.symmetric_difference_update(*others)
        return s

    def symmetric_difference_update(self, *others):
        """Update the set, keeping only elements found in either set, but not in both."""
        for o in others:
            self ^= o
        return self

    def __xor__(self, other):
        return self.symmetric_difference(other)
