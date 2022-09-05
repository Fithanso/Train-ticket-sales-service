
from abc import ABC, abstractmethod
from typing import Optional


class SeatsHandler(ABC):

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, seat_names: str, voyage) -> Optional[str]:
        pass


class AbstractSeatsHandler(SeatsHandler):

    _next_handler: SeatsHandler = None

    def set_next(self, handler: SeatsHandler) -> SeatsHandler:
        self._next_handler = handler

        return self._next_handler

    @abstractmethod
    def handle(self, seat_names: str, voyage) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(seat_names, voyage)

        return None
