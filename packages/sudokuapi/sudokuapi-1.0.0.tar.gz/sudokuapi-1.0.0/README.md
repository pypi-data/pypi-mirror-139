# SudokuAPI
A Python package for solving Sudoku puzzles.

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/alotofaxolotl/SudokuAPI)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sudokuapi)
![PyPI - License](https://img.shields.io/pypi/l/sudokuapi)
![PyPI](https://img.shields.io/pypi/v/sudokuapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sudokuapi)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/sudokuapi)

## Installation
```shell
$ pip install sudokuapi
```

## Using SudokuAPI

Start by importing the `Sudoku` class into your Python file.

```python
from sudokuapi import Sudoku
```

Then, create a 2D list to represent your sudoku puzzle, and use it to construct a new instance of the `Sudoku` class.
```python
# Can be any valid sudoku puzzle
# Use zero to indicate an empty cell
grid = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,0,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,0,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

sudoku = Sudoku(grid)
```

To solve the sudoku, simply class the `solve` method on the `Sudoku` object.

```python
sudoku.solve()
```

You can then use the `Sudoku.grid` property to access the solved Sudoku, or print it using the `print_grid` method.

```python
solution = sudoku.grid
sudoku.print_grid()
```

The output of `print_grid` looks like this.

```
5 3 4 6 7 8 9 1 2 
6 7 2 1 9 5 3 4 8 
1 9 8 3 4 2 5 6 7 
8 5 9 7 6 1 4 2 3 
4 2 6 8 5 3 7 9 1 
7 1 3 9 2 4 8 5 6 
9 6 1 5 3 7 2 8 4 
2 8 7 4 1 9 6 3 5 
3 4 5 2 8 6 1 7 9
```

The `Sudoku` class attempts to validate your sudoku using the `validate_sudoku` method. It checks that your sudoku has 9 rows and 9 columns, each containing only digits between 0 and 9. If your sudoku fails validation, `Sudoku` will print an error to the console.

```shell
Invalid Sudoku Grid: [...]
```
Then, `Sudoku` will set `grid` to `[]`, which will escape the `solve` method if it is called.