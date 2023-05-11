from Domain.film import Film
from Domain.errors import FilmError


class FilmValidator:
    """
    Valideaza un film.
    """
    @staticmethod
    def valideaza(film: Film):
        """
        Valideaza un film
        """
        err = []
        if int(film.id_entitate) < 1:
            err.append("Id-ul este invalid! ")
        if film.titlu == '':
            err.append("Titlul este invalid! ")
        if float(film.pret) <= 0:
            err.append("Pretul nu poate sa fie 0 sau negativ! ")
        if int(film.an_aparitie) > 2021 or int(film.an_aparitie) < 1800:
            err.append("Anul de aparitie este invalid! ")
        list = film.program.split("-")
        st = list[0].split(":")
        dr = list[1].split(":")
        if int(st[0]) < 0 or int(st[0]) > 23 \
                or int(st[1]) < 0 or int(st[1]) > 59:
            err.append("Ora inceperii este invalida! ")
        if int(dr[0]) < 0 or int(dr[0]) > 23 \
                or int(dr[1]) < 0 or int(dr[1]) > 59:
            err.append("Ora finala este invalida! ")
        list.clear()

        if len(err) > 0:
            raise FilmError(err)
