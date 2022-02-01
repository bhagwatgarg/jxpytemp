# JxPy

Our implementation of a compiler. The source Language is modelled after Java while the target Language will be x86. The compiler will be implemented in Python.


## Milestone 1
The documentation for our source language is present at [docs/specs.pdf](docs/specs.pdf).

## Milestone 2
To build the lexer, run `make` from the \<TOP\> directory

Test cases are present in the [tests/lexer/TestCases](tests/lexer/TestCases) directory.

To run on the binary on a test case, run, for example:

```
python3 bin/lexer.py tests/lexer/TestCases/MergeSort.java
```

The current directory structure after running `make` is:
```
.
├── bin
│   └── lexer.py
├── docs
│   └── specs.pdf
├── Makefile
├── README.md
├── src
│   └── lexer.py
└── tests
    └── lexer
        └── TestCases
            ├── BinarySearch.java
            ├── Graph.class
            ├── Graph.java
            ├── Main.java
            ├── MergeSort.class
            ├── MergeSort.java
            └── Operators.java
```


# Group Members

1. [Atharv Singh Patlan](https://github.com/athassin), 190200
2. [Bhagwat Garg](https://github.com/bhagwatgarg), 190229
3. [Rishabh Dugaye](https://github.com/rishabhd786), 190701
4. [Urbi Ghosh](https://github.com/urbighosh), 190925

Group Number : 16
