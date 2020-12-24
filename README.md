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


## Installation
`weightedset` is distributed as a standard python package through
[pypi](https://pypi.org/), so you can install it with your favourite Python
package manager. For example:

    pip install weightedset


## Usage

You can add keys to the set as many times you want. Each time you add a key,
it increases that keys weight, using a default weight of 1 if nothing is
specified.

    >>> from weightedset import WeightedSet
    >>> labels = WeightedSet()
    
    >>> labels.add("foo")
    >>> labels.add("bar", 1.5)
    >>> labels.add("baz")
    >>> labels.add("baz")
    
    >>> labels["foo"]
    1.0
    >>> labels["bar"]
    1.5
    >>> labels["baz"]
    1.5

Normal `set`-like and `dict`-like access patterns are supported where they
make sense:

    >>> labels.keys()
    ['baz', 'bar', 'foo']
    >>> "bar" in labels
    True
    >>> labels["bar"]
    1.5

The weights can be manipulated as a group:

    >>> labels *= 2
    >>> labels["bar"]
    3.0
    >>> labels.clamp(1.0)
    >>> labels["bar"]
    1.0

## Licence
This project uses the MIT licence.


## Credits
Thanks to [Oovvuu](https://oovvuu.com/) for supporting this project.

Primary authors:
* [garyd203](https://github.com/garyd203)