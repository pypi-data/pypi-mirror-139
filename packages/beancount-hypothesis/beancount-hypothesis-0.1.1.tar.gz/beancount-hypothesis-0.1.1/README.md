# beancount-hypothesis

<p align="center">
    <a href="https://github.com/jmgilman/beancount-hypothesis/actions/workflows/ci.yml">
        <img src="https://github.com/jmgilman/beancount-hypothesis/actions/workflows/ci.yml/badge.svg"/>
    </a>
    <a href="https://pypi.org/project/beancount-hypothesis">
        <img src="https://img.shields.io/pypi/v/beancount-hypothesis"/>
    </a>
</p>

> A package which provides hypothesis strategies for generating beancount types.

## Usage

Strategies are provided for all of the core types present in `beancount`. The
below example generates a random list of directives:

```python
import beancount_hypothesis as h
from hypothesis import given, strategies as s

@given(
    s.recursive(
        h.balance()
        | h.close()
        | h.commodity()
        | h.custom()
        | h.document()
        | h.event()
        | h.note()
        | h.open()
        | h.query()
        | h.pad()
        | h.price()
        | h.transaction(),
        s.lists,
        max_leaves=5,
    )
)
```

Most of the types have restrictions placed on them with the following
philosophy:

* The value shouldn't break the `beancount` package
* The value should be somewhat authentic (i.e. resemble user data)

Note that the input generated from the strategies is not intended to be passed
to any beancount functions. In other words, passing the above example to the
loader will result in undefined behavior as it doesn't follow any sensible
rules.

## Testing

```shell
tox
```

While testing a package meant for tests seems slightly redundant, there are
some custom compositions present that benefit from testing. In most cases the
tests just assert that generating data doesn't raise any exceptions (i.e. break
`beancount` in some way).

## Contributing

Check out the [issues][1] for items needing attention or submit your own and
then:

1. [Fork the repo][2]
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

[1]: https://github.com/jmgilman/beancount-hypothesis/issues
[2]: https://github.com/jmgilman/beancount-hypothesis/fork
