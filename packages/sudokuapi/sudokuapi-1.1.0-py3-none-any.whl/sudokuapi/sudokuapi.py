class Sudoku:

    def validate_grid(self, grid: list) -> bool:

        # If there are not 9 rows, it is not a valid grid
        if len(grid) != 9:
            return False

        for row in grid:
            # If a row does not have 9 columns, it is not a valid grid
            if len(row) != 9:
                return False

            for digit in row:
                # If a row contains a non-integer or an invalid digit, it is invalid
                if digit not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    return False

        return True

    def __init__(self, grid: list) -> None:
        
        self.solved = False

        if self.validate_grid(grid):
            self.grid = grid
        else:
            print(f'Invalid Sudoku Grid: {grid}')
            self.grid = []

    # Can a number n be legally inserted at position x, y
    def possible(self, y, x, n) -> bool:

        # Check for n in row
        if n in self.grid[y]:
            return False

        # Check for n in column
        if n in [row[x] for row in self.grid]:
            return False

        # Use floor division to round x, y to nearest square
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        # Check for n in square
        for i in range(3):
            for j in range(3):
                if self.grid[y0+i][x0+j] == n:
                    return False

        return True

    # print the sudoku grid
    def print_grid(self):
        for row in self.grid:
            row_string = ''
            for digit in row:
                row_string += f'{digit} '
            print(row_string)

    # Use recursion and backtracking to solve the grid
    def solve(self):

        # Iterate over the grid
        for y in range(9):
            for x in range(9):

                # If the current cell is empty
                if self.grid[y][x] == 0:

                    # Assign the next possible value
                    for n in range(1, 10):
                        if self.possible(y, x, n):

                            # Insert that value
                            self.grid[y][x] = n
                            # Solve recursively
                            self.solve()
                            # If the solution fails, backtrack
                            if not self.solved:
                                self.grid[y][x] = 0
                    return
        self.solved = True