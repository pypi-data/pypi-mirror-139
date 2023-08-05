import random
from dataclasses import dataclass, field

from hypothesis import strategies
from random_words import RandomWords  # type: ignore


@dataclass
class AccountGenerator:
    """A class for generating semi-realistic account structures.

    This class provides a single method, generate(), which will create a list
    of nested accounts. The final result is intended to look semi-realistic in
    the sense that account names use real words and typically have one or more
    subaccounts (except for the leaves). The class attributes can be modified
    in order to control how the structure is generated.

    Attributes:
        min_leaves: The minimum number of leaves to generate for each node
        max_leaves: The maximum number of leaves to generate for each node
        min_nodes: The minimum number of nodes to generate for each leaf
        max_nodes: The max number of nodes to generate for each leaf
    """

    min_leaves: int = 1
    max_leaves: int = 3
    min_nodes: int = 3
    max_nodes: int = 5
    rw: RandomWords = field(default_factory=RandomWords)

    def generate(self) -> list[str]:
        """Generates a list of semi-realistic account names.

        Example:
        [
            "Inquiry:Bars",
            "Inquiry:Entrance",
            "Inquiry:Introduction",
            "Successes:Armament",
            "Successes:Rail:Flares",
            "Successes:Rail:Spindle",
            "Successes:Rail:Ones",
            "Successes:Presses",
            "Successes:Waste:Hugs",
            "Successes:Waste:Catcher",
            "Successes:Waste:Signs",
            "Beams:Failure",
            "Beams:Cylinder",
            "Beams:Kiss",
            "Beams:Diseases"
        ]
        """
        accounts: list[str] = []
        for segments in _walk_dict(self._make_tree()):
            accounts.append(":".join(segments))

        return accounts

    def _make_tree(self, depth=0):
        """Generates a nested tree structure using random words as keys."""
        if depth >= self.max_leaves:
            return None

        names = self._rand_words()
        d = dict.fromkeys(names)
        for name in names:
            d[name] = self._make_tree(depth + self._rand_leave())

        return d

    def _rand_leave(self) -> int:
        """Generates a random number of leaves to generate."""
        if self.min_leaves == self.max_leaves:
            return 1
        else:
            return random.randrange(self.min_leaves, self.max_leaves)

    def _rand_node(self) -> int:
        """Generates a random number of nodes to generate."""
        if self.min_nodes == self.max_nodes:
            return self.min_nodes
        else:
            return random.randrange(self.min_nodes, self.max_nodes)

    def _rand_words(self) -> list[str]:
        """Generates a random number of words as configured by the class."""
        return [
            w.capitalize()
            for w in self.rw.random_words(count=self._rand_node())
        ]


@strategies.composite
def account_name(_) -> str:
    """Generates a random account name.

    Returns:
        A random account name.
    """
    ag = AccountGenerator(min_nodes=1, max_nodes=1, min_leaves=3, max_leaves=3)
    return ag.generate()[0]


def _walk_dict(d: dict, pre: list | None = None):
    """Walks the keys of the given dictionary, returning leaves as lists.

    This function will recursively walk a nested dictionary and generate a list
    of keys for all leaves contained within the nested structure. The given
    structure should only contain nested dictionaries and leaf values are
    discarded as this function is only concerned with dictionary keys.

    Args:
        d: The dictionary to walk
        pre: Used in recursion

    Yields:
        Lists for each leaf contained within the structure.

        For example:

            {
                "one":{
                    "two":{
                        "three": None
                    }
                },
                "four":{
                    "five":{
                        "six": None
                    }
                }
            }

        Would yield:

            ['one', 'two', 'three']
            ['four', 'five', 'six']
    """
    pre = pre[:] if pre else []
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                for d in _walk_dict(value, pre + [key]):
                    yield d
            else:
                yield pre + [key]
    else:
        yield pre + [d]
