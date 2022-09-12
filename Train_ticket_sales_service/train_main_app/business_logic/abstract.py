from abc import ABC, abstractmethod
from typing import Optional

from django.http import Http404
from django.shortcuts import redirect


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


class ParamValidator(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


class ViewHandler(ABC):

    # where user should end up if view gets wrong parameters
    redirect_to_if_invalid = ''

    @abstractmethod
    def get(self):
        pass

    def redirect_if_invalid(self):
        if self.redirect_to_if_invalid:
            return redirect(self.redirect_to_if_invalid)
        else:
            raise Http404()

