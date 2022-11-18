from abc import ABC, abstractmethod
from typing import Optional


class Validator(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, seat_numbers, voyage) -> Optional[str]:
        pass


class AbstractSeatsValidator(Validator):

    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, seat_numbers, voyage) -> str:
        if self._next_handler:
            return self._next_handler.handle(seat_numbers, voyage)

        return None


class ParamValidator(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs):
        pass