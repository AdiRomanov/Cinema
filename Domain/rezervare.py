from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Rezervare(Entitate):
    """
    Descrie o entitate
    """
    id_film_r: str
    id_card_client: str
    data: str
    ora: str
