"""
This module contains code for an abstract base class of builder.
Builder is to support builder pattern.
"""

from abc import ABC, abstractmethod
from typing import Any


class BuilderAbstract(ABC):
    """
    An abstract class to best represent an interface for builder design pattern.

    Arguments:
        self
    """
    result: Any

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def build(self, **kwargs) -> None:
        """
        This method builds an instance of the class that builder is specifically
        implemented to and stores the result as self.result
        Arguments:
            self
            **kwargs
                Keyword args used to build object.
        Returns:
            None
        """

    @abstractmethod
    def get(self, **kwargs) -> Any:
        """
        Gets result if not None, else calls build then returns it.

        Arguments:
            self
            **kwargs
                Keyword args that can be passed to build()
        Returns:
            Any
                Implementing classes can override to provide a more specific type.
        """

class BuilderBase(BuilderAbstract):
    """
    Intended to be inherited by most specific builder implementations.
    Implements __init__ and get methods as they are likely to be the same in
    95% of cases. 

    Arguments:
        self
    """
    def __init__(self):
        self.result = None

    @abstractmethod
    def build(self, **kwargs) -> None:
        pass

    def get(self, **kwargs) -> Any:
        if self.result is None:
            self.build(**kwargs)
        return self.result
