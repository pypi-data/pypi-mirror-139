from typing import Optional
from math import sqrt

Number = Optional[float]

class Calculator:
  """A Program that define a Basic Calculator

  The Program implements the add, minus, multipy, divide and root
  to receive an optional argument. If the argument is not provided
  the chosen operation is done on the in memory value of the calculator

  >>> calc = Calculator()
  >>> calc.add(5)
  5.0
  >>> calc.minus(2.3)
  2.7
  >>> calc.answer
  2.7
  >>> calc.reset()  # reset calculator memory to zero 0
  >>> calc.root(-1) # return '0' for complex number
  0
  >>> calc.root(4)
  2.0
  >>> calc.multiply(7)
  14.0
  >>> calc.divide(2)
  7.0
  """
  def __init__(self) -> None:
    self._answer=float(0)

  def reset(self) -> None:
    """ reset calculator answer to zero"""
    self._answer = float(0)

  
  def add(self, x: Number=None) -> Number:
    """ Increment value in answer by 'x' """
    self._answer += x or self._answer
    return self._answer
  
  def minus(self, x: Number=None) -> Number:
    """ Decrement value in answer by 'x' """
    self._answer -= x or self._answer
    return self._answer
  
  def multiply(self, x: Number=None) -> Number:
    """ Multiply value in answer by 'x' """
    self._answer *= x or self._answer
    return self._answer
  
  def divide(self, x: Number=None) -> Number:
    """ Divide value in answer by 'x' """
    self._answer /= x or self._answer
    return self._answer
  
  def root(self, x: Number=None) -> Number:
    """ Finds the root of  'x' """
    value= x or self._answer
    if value < 0:
      return 0
    self._answer = sqrt(value)
    return self._answer
  
  @property
  def answer(self):
    return self._answer