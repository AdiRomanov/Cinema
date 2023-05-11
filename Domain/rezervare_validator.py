from Domain.errors import RezervareError
from Domain.rezervare import Rezervare


class RezervareValidator:
    """
        Valideaza o rezervare.
    """

    @staticmethod
    def valideaza(rezervare: Rezervare):
        err = []
        if int(rezervare.id_entitate) < 1:
            err.append("Id-ul nu poate sa fie negativ sau 0!")
        if int(rezervare.id_film_r) < 1:
            err.append("Id-ul filmului nu poate sa fie negativ sau 0!")
        if int(rezervare.id_card_client) < 0:
            err.append("Id-ul cardului nu poate sa fie negativ !")
        list = rezervare.data.split(".")
        if int(list[0]) < 1 or int(list[0]) > 31:
            err.append("Data rezervarii invalida!")
        elif int(list[1]) < 1 or int(list[1]) > 12:
            err.append("Data rezervarii invalida!")
        elif int(list[2]) < 1900 or int(list[2]) > 2021:
            err.append("Data rezervarii invalida!")
        list.clear()
        list = rezervare.ora.split(":")
        if int(list[0]) < 0 or int(list[0]) > 24:
            err.append("Ora rezervarii invalida!")
        elif int(list[1]) < 0 or int(list[1]) > 59:
            err.append("Ora rezervarii invalida!")

        if len(err) > 0:
            raise RezervareError(err)
