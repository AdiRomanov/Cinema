from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class User(Entitate):
    """
    Descrie un film.
    """
    username: str
    email: str
    password: str

