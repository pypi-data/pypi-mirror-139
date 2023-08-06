from typing import Union, Optional
import numbers

Number = Union[int, float]
Number2 = Optional[Union[int, float]]


class Calculator:
    """ Calculator for basic math functions

        Implemented methods:
                            addition
                            subtraction
                            multiplication
                            division
                            nth-root ((n) root of a number)

        Result is stored and overwritten in memory until reset() method is ran.

        Calculation methods can take either one or two arguments (in addition to self).
        If only one arguments is given calculations will be performed with memory value (latest result),
        otherwise calculations will be performed between two arguments and memory value will be overwritten.

        For example:

        >>> calc = Calculator()
        >>> calc.addition(4, 5)
        9
        >>> calc.addition(10)
        19
        >>> calc.multiplication(2)
        38
        >>> calc.multiplication(2, 5)
        10
        >>> calc.reset()
        0
    """

    def __init__(self):
        self.memory = 0

    def addition(self, x: Number, y: Number2=None) -> Union[int, float]:
        """ With single argument, return addition of self and x

            y (optional)
                With two arguments, return addition of x an y
        """
        self._input_validation(x, y)
        if not y:
            self.memory += x
        else:
            self.memory = x + y
        return self.memory

    def subtraction(self, x: Number, y: Number2=None) -> Union[int, float]:
        """ With single argument, return subtraction of self and x

            y (optional)
                With two arguments, return subtraction of x an y
        """
        self._input_validation(x, y)
        if not y:
            self.memory -= x
        else:
            self.memory = x - y
        return self.memory

    def multiplication(self, x: Number, y: Number2=None) -> Union[int, float]:
        """ With single argument, return multiplication of self and x

            y (optional)
                With two arguments, return multiplication of x an y
        """
        self._input_validation(x, y)
        if not y:
            self.memory *= x
        else:
            self.memory = x * y
        return self.memory

    def division(self, x: Number, y: Number2=None) -> float:
        """ With single argument, return division of self and x

            y (optional)
                With two arguments, return division of x an y
        """
        self._input_validation(x, y)
        if y is None:
            if not x:
                raise ZeroDivisionError('Cannot divide by zero!')
            else:
                self.memory /= x
        else:
            if not y:
                raise ZeroDivisionError('Cannot divide by zero!')
            else:
                self.memory = x / y
        return self.memory

    def nth_root(self, x: int, n: Number2=None) -> float:
        """ With single argument, return x'th root of self

            y (optional)
                With two arguments, return n'th root of x
        """
        self._input_validation(x, n)
        if n is None:
            if not x:
                self.memory = float('inf')
            elif self.memory < 0:
                raise ValueError('Complex numbers are not supported')
            else:
                self.memory = self.memory**(1 / x)
        else:
            if not n:
                self.memory = float('inf')
            elif x < 0:
                raise ValueError('Complex numbers are not supported')
            else:
                self.memory = x**(1 / n)
        return self.memory

    def reset(self) -> int:
        """ Reset memory to int(0)"""
        self.memory = 0
        return self.memory

    def _input_validation(self, x: Number, y: Number2=None):
        """ Check that user input is a number"""
        if not y:
            if not isinstance(x, numbers.Number):
                raise TypeError(f'Provided input is not a number')
        else:
            if not all(isinstance(i, numbers.Number) for i in [x, y]):
                raise TypeError(f'Provided input is not a number')


if __name__ == '__main__':
    import doctest

    print(doctest.testmod())

