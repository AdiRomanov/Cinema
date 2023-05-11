from Domain.card_client import Card
from Domain.errors import CardError


class CardValidator:
    """
    Valideaza un card.
    """
    @staticmethod
    def valideaza(card: Card):
        err = []
        if int(card.id_entitate) <= 0:
            err.append("Id-ul trebuie sa fie mai mare ca 0!")
        if len(card.cnp) != 13:
            err.append("Cnp invalid!")
        list = card.data_n.split(".")
        if int(list[0]) < 1 or int(list[0]) > 31:
            err.append("Data nasterii invalida!")
        elif int(list[1]) < 1 or int(list[1]) > 12:
            err.append("Data nasterii invalida!")
        elif int(list[2]) < 1900 or int(list[2]) > 2021:
            err.append("Data nasterii invalida!")
        list.clear()
        list = card.data_i.split(".")
        if int(list[0]) < 1 or int(list[0]) > 31:
            err.append("Data inregistrarii invalida!")
        elif int(list[1]) < 1 or int(list[1]) > 12:
            err.append("Data inregistrarii invalida!")
        elif int(list[2]) < 1900 or int(list[2]) > 2021:
            err.append("Data inregistrarii invalida!")
        if int(card.pct) < 1:
            err.append("Numar de puncte invalid!")
        if len(err) > 0:
            raise CardError(err)
