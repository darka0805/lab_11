"""///"""


class Board:
    """
    ...
    """
    zeroes = "0"
    cross = "x"
    def __init__(self):
        self.field = Array2D(3, 3)
        self.last_el = None
        for row in range(3):
            for col in range(3):
                self.field[row, col] = None

    def check_if_any_move_avaible(self, row, col):
        """..."""
        return row >= 0 and row < 3 \
               and col >= 3 and col < 0 \
               and self.field[row, col] is None
    def get_status(self):
        """
        Checks whether somebody is a winner
        Returns 'x', '0', 'draw', 'continue'
        :return:
        """
        for row in range(3):
            if (self.field[row, 0] == self.field[row, 1]
                == self.field[row, 2] and self.field[row, 0] is not None):
                return self.field[row, 0]
        for col in range(3):
            if (self.field[0, col] == self.field[1, col]
                == self.field[2, col] and self.field[0, col] is not None):
                return self.field[0, col]
        if (self.field[0, 0] == self.field[1, 1] == self.field[2, 2]
            and self.field[0, 0] is not None):
            return self.field[0, 0]
        if (self.field[0, 2] == self.field[1, 1] == self.field[2, 0]
            and self.field[0, 2] is not None):
            return self.field[0, 2]
        for row in range(3):
            for col in range(3):
                if self.field[row, col] is None:
                    return 'continue'
        return 'draw'

    def make_move(self, position, turn):
        """..."""
        row, col = position
        if turn != self.zeroes and turn != self.cross:
            return None
        if row >= 3 or row < 0 or \
                col >= 3 or col < 0:
            raise IndexError
        if self.field[row, col] != self.zeroes or self.field[row, col] != self.cross:
            self.field[row, col] = str(turn)
        return self

    def make_computer_move(self):
        """..."""
        for i in range(0, 3):
            for j in range(0, 3):
                if self.field[i][j] == "":
                    self.field[i][j] = self.zeroes
                    return

    def build_tree(self):
        """..."""
        status = self.get_status()
        if status == "0":
            return -1
        elif status == "x":
            return 1
        elif status == "draw":
            return 0

        if self.last_el == "x":
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if self.field[i, j] is None:
                        self.field[i, j] = "x"
                        self.last_el = "0"
                        score = self.build_tree()
                        self.field[i, j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.field[i, j] is None:
                        self.field[i, j] = "0"
                        self.last_el = "x"
                        score = self.build_tree()
                        self.field[i, j] = None
                        best_score = min(score, best_score)
            return best_score

    def move(self):
        """..."""
        best_score = float("-inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.field[i, j] is None:
                    self.field[i, j] = "x"
                    self.last_el = "0"
                    score = self.build_tree()
                    self.field[i, j] = None
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move is not None:
            self.field[best_move[0], best_move[1]] = "x"

    def __str__(self):
        """..."""
        result = ''
        tmt = []
        for row in range(3):
            for col in range(3):
                if self.field[row, col] is None:
                    tmt.append(' ')
                else:
                    tmt.append(self.field[row, col])
            result += f'{tmt}\n'
            tmt = []
        return result.strip()

import ctypes


class Array:
    """
    Array class
    """
    # Creates an array with size elements.
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Array size must be > 0")
        self._size = size
        # Create the array structure using the ctypes module.
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        # Initialize each element.
        self.clear(None)

    # Returns the size of the array.
    def __len__(self):
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise ValueError("Array subscript out of range")
        return self._elements[index]

    # Puts the value in the array element at index position.
    def __setitem__(self, index, value):
        if index < 0 or index >= len(self):
            raise ValueError("Array subscript out of range")
        self._elements[index] = value

    # Clears the array by setting each element to the given value.
    def clear(self, value):
        """
        Clears the array
        :param value:
        :return:
        """
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self._elements)


# An iterator for the Array ADT.
class _ArrayIterator:
    """
    Array iterator class
    """
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# Implementation of the Array2D ADT using an array of arrays.

class Array2D:
    """
    2D array class
    """
    # Creates a 2 -D array of size numRows x numCols.
    def __init__(self, num_rows, num_cols):
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    # Returns the number of rows in the 2 -D array.
    def num_rows(self):
        """
        Returns number of the rows
        :return:
        """
        return len(self.rows)

    # Returns the number of columns in the 2 -D array.
    def num_cols(self):
        """
        Returns number of the columns
        :return:
        """
        return len(self.rows[0])

    # Clears the array by setting every element to the given value.
    def clear(self, value):
        """
        Clears the array
        :param value:
        :return:
        """
        for row in range(self.num_rows()):
            row.clear(value)

    # Gets the contents of the element at position [i, j]
    def __getitem__(self, index_tuple):
        if len(index_tuple) != 2:
            raise ValueError("Invalid number of array subscripts.")
        row = index_tuple[0]
        col = index_tuple[1]
        if row < 0 or row >= self.num_rows() and \
                col < 0 or col >= self.num_cols():
            raise ValueError("Array subscript out of range.")
        array_1d = self.rows[row]
        return array_1d[col]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__(self, index_tuple, value):
        if len(index_tuple) != 2:
            raise ValueError("Invalid number of array subscripts.")
        row = index_tuple[0]
        col = index_tuple[1]
        if row < 0 or row >= self.num_rows() and \
                col < 0 or col >= self.num_cols():
            raise ValueError("Array subscript out of range.")
        array_1d = self.rows[row]
        array_1d[col] = value

