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

## Milestone 3
To build the parser, run `make` from the \<TOP\> directory

Test cases are present in the [tests/parser/TestCases](tests/parser/TestCases) directory.

To run the binary on a test case, run, for example:

```
python3 bin/parser.py tests/parser/TestCases/MergeSort.java
```

To generate a graph, run:
```
python3 bin/create_graph.py
```
The file `graph.png` will be generated in `bin/` directory.

The current directory structure after running `make` is:
```
.
├── bin
├── docs
│   └── specs.pdf
├── Makefile
├── README.md
├── src
│   ├── create_graph.py
│   ├── lexer.py
│   └── parser.py
└── tests
    ├── lexer
    │   └── TestCases
    │       ├── BinarySearch.java
    │       ├── Graph.java
    │       ├── Main.java
    │       ├── MergeSort.java
    │       └── Operators.java
    └── parser
        └── TestCases
            ├── BinarySearch.java
            ├── Graph.java
            ├── Main.java
            ├── MergeSort.java
            ├── Operators.java
            └── SyntaxError.java


```


# Group Members

1. [Atharv Singh Patlan](https://github.com/athassin), 190200
2. [Bhagwat Garg](https://github.com/bhagwatgarg), 190229
3. [Rishabh Dugaye](https://github.com/rishabhd786), 190701
4. [Urbi Ghosh](https://github.com/urbighosh), 190924

Group Number : 16
