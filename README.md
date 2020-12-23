# weightedset: A Weighted Set implementation for Python. 

<p align="center">
    <a href="https://pypi.org/project/weightedset/">
        <img src="https://img.shields.io/pypi/v/weightedset.svg" alt="Package version">
    </a>
    <a href="https://pypi.org/project/weightedset/">
        <img src="https://img.shields.io/pypi/pyversions/weightedset.svg" alt="Python versions">
    </a>
    <a href="https://pypi.org/project/weightedset/">
        <img src="https://img.shields.io/pypi/dm/weightedset.svg" alt="Monthly downloads">
    </a>
</p>

A Weighted Set is a collection of unique keys with attached weights. Keys can
be assigned a different (positive) numeric value.

* A weighted set is not a normal set, because each item in the set has a
  different weight.
* A weighted set is like a multi-set, except the weights do not have to be
  integers (whole numbers).
* A weighted set is not a dictionary, because the values can only be weights,
  along with special semantics for adding duplicate keys.