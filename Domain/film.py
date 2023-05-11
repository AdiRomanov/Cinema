from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Film(Entitate):
    """
    Descrie un film.
    """
    titlu: str
    an_aparitie: str
    pret: float
    program: str
