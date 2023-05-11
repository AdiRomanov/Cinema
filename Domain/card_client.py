from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Card(Entitate):
    """
    Descrie un card de fidelitate.
    """
    nume: str
    prenume: str
    cnp: str
    data_n: str
    data_i: str
    pct: float
