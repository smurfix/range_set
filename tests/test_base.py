from range_set import RangeSet
from itertools import permutations
import pytest

_test_create = (
    ((1, 2, 3, 4), [(1, 5)]),
    ((1, 2, 3, 5), [(1, 4), (5, 6)]),
    (((1, 4), (5, 6)), [(1, 4), (5, 6)]),
    (((1, 5), (5, 6)), [(1, 6)]),
    (((1, 5), (2, 3)), [(1, 5)]),
    (((1, 5), (2, 6)), [(1, 6)]),
    (((1, 5), (0, 4)), [(0, 5)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (7, 8)), [(1, 3), (5, 6), (7, 8), (10, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (7, 8)), [(1, 3), (5, 6), (7, 8), (10, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (7, 10)), [(1, 3), (5, 6), (7, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (6, 8)), [(1, 3), (5, 8), (10, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (6, 10)), [(1, 3), (5, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (4, 11)), [(1, 3), (4, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (0, 10)), [(0, 12), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (0, 13)), [(0, 13), (14, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (0, 17)), [(0, 17)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (11, 15)), [(1, 3), (5, 6), (10, 16)]),
    (((1, 3), (5, 6), (10, 12), (14, 16), (11, 18)), [(1, 3), (5, 6), (10, 18)]),
)

_test_remove = (
    ((), (1, 3), []),
    (((2, 4),), (1, 3), [(3, 4)]),
    (((2, 4),), (1, 4), []),
    (((2, 4),), (1, 5), []),
    (((2, 4),), (2, 5), []),
    (((2, 4),), (3, 5), [(2, 3)]),
    (((2, 4), (6, 8)), (3, 6), [(2, 3), (6, 8)]),
    (((2, 4), (6, 8)), (1, 6), [(6, 8)]),
    (((2, 4), (6, 8)), (3, 9), [(2, 3)]),
    (((0, 1), (2, 4), (6, 8)), (3, 6), [(0, 1), (2, 3), (6, 8)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (3, 6), [(0, 1), (2, 3), (6, 8), (10, 11)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (1, 9), [(0, 1), (10, 11)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (0, 9), [(10, 11)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (-1, 9), [(10, 11)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (3, 10), [(0, 1), (2, 3), (10, 11)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (3, 11), [(0, 1), (2, 3)]),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (0, 11), []),
    (((0, 1), (2, 4), (6, 8), (10, 11)), (1, 11), [(0, 1)]),
)

_test_disjoint = (
    ((), (), True),
    (((0, 1),), (), True),
    (((0, 1),), ((1, 2),), True),
    (((0, 2),), ((1, 2),), False),
    (((0, 2), (4, 5)), ((2, 3),), True),
    (((0, 2), (4, 5)), ((2, 4),), True),
    (((0, 2), (4, 5)), ((1, 4),), False),
    (((0, 2), (4, 5)), ((2, 5),), False),
    (((0, 2), (4, 5)), ((4, 6),), False),
    (((0, 2), (4, 5)), ((4, 6), (7, 8)), False),
    (((0, 2), (4, 5)), ((5, 6), (7, 8)), True),
)


def test_create():
    for i, o in _test_create:
        for ii in permutations(i):
            c = RangeSet(ii)
            assert list(c) == o, (ii, o)


def test_remove():
    for i, r, o in _test_remove:
        c = RangeSet(i)
        try:
            if isinstance(r, tuple):
                c.remove(*r)
            else:
                c.remove(r)
        except KeyError:
            assert list(i) == o
        assert list(c) == o, (i, r, o)


def test_disjoint():
    for i, j, o in _test_disjoint:
        i = RangeSet(i)
        j = RangeSet(j)
        assert o == i.isdisjoint(j)
        assert o == j.isdisjoint(i)


cs = RangeSet((2, 5, 6, 7, 9, 10))


def test_inside():
    assert 0 not in cs
    assert 1 not in cs
    assert 2 in cs
    assert 3 not in cs
    assert 4 not in cs
    assert 5 in cs
    assert 6 in cs
    assert 7 in cs
    assert 8 not in cs
    assert 9 in cs
    assert 10 in cs
    assert 11 not in cs
    assert 12 not in cs


def test_presence():
    assert not cs.present(1, 3)
    assert cs.present(2, 3)
    assert not cs.present(2, 4)
    assert not cs.present(2, 6)
    assert cs.present(5, 6)
    assert cs.present(5, 8)
    assert not cs.present(5, 9)
    assert not cs.present(5, 10)


def test_absence():
    assert cs.absent(1, 2)
    assert not cs.absent(1, 3)
    assert not cs.absent(2, 3)
    assert not cs.absent(2, 4)
    assert cs.absent(3, 4)
    assert cs.absent(3, 5)
    assert not cs.absent(3, 6)


def test_pop():
    c = RangeSet((1, 2, 5, 6, 7))
    assert c.pop() == 7
    assert c.pop() == 6
    assert c.pop() == 5
    assert c.pop() == 2
    assert c.pop() == 1
    with pytest.raises(KeyError):
        assert c.pop()


def test_len():
    c = RangeSet()
    assert len(c) == 0
    assert len(cs) == 3
    assert cs.count() == 6


def test_cmp_etc():
    b = RangeSet((1, 3))
    c = RangeSet((1, 3, 4, 5, 7, 8))
    d = RangeSet((3, 4, 7, 8))
    e = RangeSet((3, 4, 7, 8, 9))
    f = RangeSet((3, 4, 7, 8, 10))
    g = RangeSet((4, 7, 8, 10))

    assert b.span() == RangeSet(((1, 4),))
    assert c.span() == RangeSet(((1, 9),))
    assert g.span() == RangeSet(((4, 11),))

    assert c & g == RangeSet((4, 7, 8))
    assert c | g == RangeSet((1, 3, 4, 5, 7, 8, 10))
    assert b.isdisjoint(g)
    assert not b.isdisjoint(e)

    assert d < c
    assert d <= c
    assert not d > c
    assert not d >= c
    assert c <= c
    assert c > d
    assert c >= d
    assert not c < d
    assert not c <= d
    assert c != d
    assert d != c
    assert c != f
    assert f != c
    assert not (c > f)
    assert not (c >= f)
    assert not (c < f)
    assert not (c <= f)
    assert not (f > c)
    assert not (f >= c)
    assert not (f < c)
    assert not (f <= c)

    assert c.issubset(c)
    assert not c.issubset(c, proper=True)

    assert not c.issubset(f, proper=False)
    assert not c.issubset(f, proper=True)
    assert not f.issubset(c, proper=False)
    assert not f.issubset(c, proper=True)

    assert not c.issubset(d, proper=False)
    assert not c.issubset(d, proper=True)
    assert d.issubset(c, proper=False)
    assert d.issubset(c, proper=True)

    assert c.issuperset(c)
    assert not c.issuperset(c, proper=True)

    assert not c.issuperset(f, proper=False)
    assert not c.issuperset(f, proper=True)
    assert not f.issuperset(c, proper=False)
    assert not f.issuperset(c, proper=True)

    assert c.issuperset(d, proper=False)
    assert c.issuperset(d, proper=True)
    assert not d.issuperset(c, proper=False)
    assert not d.issuperset(c, proper=True)

    assert c == RangeSet((1, 3, 4, 5, 7, 8))
    assert d == RangeSet((3, 4, 7, 8))
    assert e == RangeSet((3, 4, 7, 8, 9))
    assert f == RangeSet((3, 4, 7, 8, 10))


def test_union():
    c = RangeSet((1, 3, 4, 5, 7, 8))
    d = RangeSet((3, 4, 7, 8))
    e = RangeSet((3, 4, 7, 8, 9))
    f = RangeSet((1, 3, 4, 5, 7, 8, 9))
    g = RangeSet((5, 7))
    h = RangeSet((1,))

    assert c.union(d) == c
    assert d.union(c) == c
    assert c.union(e) == f
    assert e.union(c) == f
    assert d.union(h, g) == c
    assert d.union(g, h) == c
    assert g.union(h, d) == c
    assert g.union(d, h) == c
    assert h.union(g, d) == c
    assert h.union(d, g) == c

    assert c | d == c
    assert d | c == c
    assert c | e == f

    assert d == RangeSet((3, 4, 7, 8))
    assert e == RangeSet((3, 4, 7, 8, 9))

    dd = d
    d |= c
    assert dd is d
    assert d is not c
    assert d == c

    e.union_update(g, h)
    assert e == f

    assert c == RangeSet((1, 3, 4, 5, 7, 8))
    assert g == RangeSet((5, 7))
    assert h == RangeSet((1,))
    assert f == RangeSet((1, 3, 4, 5, 7, 8, 9))


def test_intersection():
    c = RangeSet((1, 3, 4, 5, 7, 8))
    d = RangeSet((3, 4, 7, 8))
    e = RangeSet((3, 4, 7, 8, 9))
    f = RangeSet((1, 3, 4, 5, 7, 8, 9))
    g = RangeSet((5, 7))
    h = RangeSet((1,))

    assert c.intersection(d) == d
    assert d.intersection(c) == d
    assert c.intersection(e) == d
    assert e.intersection(c) == d
    assert f.intersection(e, g) == RangeSet((7,))

    assert c & d == d
    assert d & c == d
    assert c & e == d

    assert c == RangeSet((1, 3, 4, 5, 7, 8))
    assert f == RangeSet((1, 3, 4, 5, 7, 8, 9))
    assert g == RangeSet((5, 7))
    assert h == RangeSet((1,))

    cx = c.copy()
    cc = c
    c &= d
    assert cc is c
    assert c is not d
    assert c == d

    cx.intersection_update(e, g)
    assert cx == RangeSet((7,))

    f.intersection_update(e)
    assert f == e

    assert d == RangeSet((3, 4, 7, 8))
    assert e == RangeSet((3, 4, 7, 8, 9))

    assert e == RangeSet((3, 4, 7, 8, 9))


def test_difference():
    c = RangeSet((1, 3, 4, 5, 7, 8))
    d = RangeSet((3, 4, 7, 8))
    e = RangeSet((3, 4, 7, 8, 9))
    f = RangeSet((1, 3, 4, 5, 7, 8, 9))
    g = RangeSet((5,))
    h = RangeSet((1,))

    assert c.difference(d, h) == g
    assert d.difference(c) == RangeSet()
    assert f.difference(f) == RangeSet()
    assert d.difference(f) == RangeSet()
    assert c.difference(d, g) == h

    assert c - d - h == g
    assert d - c == RangeSet()
    assert f - f == RangeSet()
    assert g - h == g
    assert h - g == h

    assert c == RangeSet((1, 3, 4, 5, 7, 8))
    assert f == RangeSet((1, 3, 4, 5, 7, 8, 9))
    assert g == RangeSet((5,))
    assert h == RangeSet((1,))

    cc = c
    c -= g | h
    assert cc is c
    assert c is not d
    assert c == d

    ff = f.copy()
    f.difference_update(e)
    assert f == g | h

    ff.difference_update(g, h)
    assert ff == e

    assert d == RangeSet((3, 4, 7, 8))
    assert e == RangeSet((3, 4, 7, 8, 9))


def test_symmetric_difference():
    c = RangeSet((1, 3, 4, 5, 7, 8))
    d = RangeSet((3, 4, 7, 8))
    e = RangeSet((3, 4, 7, 8, 9))
    f = RangeSet((1, 3, 4, 5, 7, 8, 9))
    g = RangeSet((5,))
    h = RangeSet((1,))

    assert c.symmetric_difference(f) == RangeSet((9,))
    assert f.symmetric_difference(c) == RangeSet((9,))
    assert c.symmetric_difference(d, h) == g
    assert e.symmetric_difference(f) == g | h
    assert e.symmetric_difference(f, g) == h
    assert e.symmetric_difference(f, h) == g
    assert e.symmetric_difference(g, h) == f
    assert f.symmetric_difference(g, h) == e
    assert d.symmetric_difference(d) == RangeSet()

    assert c ^ d ^ h == g
    assert e ^ f == g | h

    assert c == RangeSet((1, 3, 4, 5, 7, 8))
    assert f == RangeSet((1, 3, 4, 5, 7, 8, 9))
    assert g == RangeSet((5,))

    gx = g.copy()
    gg = g
    g ^= c ^ h
    assert gg is g
    assert g is not d
    assert g == d

    ff = f.copy()
    f.symmetric_difference_update(e)
    assert f == gx | h

    ff.symmetric_difference_update(gx, h)
    assert ff == e

    assert d == RangeSet((3, 4, 7, 8))
    assert e == RangeSet((3, 4, 7, 8, 9))
    assert gx == RangeSet((5,))
    assert h == RangeSet((1,))
