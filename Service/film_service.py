import random
import string

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self, film_repository: Repository,
                 film_validator: FilmValidator,
                 rezervare_repository: Repository = None,
                 undo_redo_service: UndoRedoService = None):
        self.__film_repository = film_repository
        self.__film_validator = film_validator
        self.__rezervare_repository = rezervare_repository
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        :return: Lista de filme
        """
        return self.__film_repository.read()

    def adauga(self, id_entitate, titlu, an_aparitie, pret, program):
        """
        Adauga un film in lista
        """
        film = Film(id_entitate, titlu, an_aparitie, pret, program)
        self.__film_validator.valideaza(film)
        self.__film_repository.adauga(film)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service.add_undo_operation(
                AddOperation(self.__film_repository, film))

    def sterge(self, id_entitate):
        """
        Sterge un film din lista
        """
        film = self.__film_repository.read(id_entitate)
        self.__film_repository.sterge(id_entitate)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service. \
                add_undo_operation(DeleteOperation
                                   (self.__film_repository,
                                    film))

    def modifica(self, id_entitate, titlu, an_aparitie, pret, program):
        """
        Modifica un film din lista
        """
        film_anterior = self.__film_repository.read(id_entitate)
        film = Film(id_entitate, titlu, an_aparitie, pret, program)
        self.__film_validator.valideaza(film)
        self.__film_repository.modifica(film)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service. \
                add_undo_operation(ModifyOperation
                                   (self.__film_repository,
                                    film,
                                    film_anterior))

    def film_random(self, numar_filme):
        """
        Metoda care genereaza un numar dat de filme random
        """
        try:
            while numar_filme:
                id_entitate = random.randint(1, 1000)
                if self.__film_repository.read(str(id_entitate)) is None:
                    letters = string.ascii_lowercase
                    titlu = ''.join(random.choice(letters) for _ in range(10))
                    titlu = titlu.capitalize()
                    an_aparitie = random.randint(1800, 2021)
                    pret = random.randint(1, 300)
                    ora1 = random.randint(0, 23)
                    min1 = random.randint(0, 59)
                    ora2 = random.randint(0, 23)
                    min2 = random.randint(0, 59)
                    program = str(ora1) + ":" + str(min1) + " - "
                    program += str(ora2) + ":" + str(min2)
                    film = Film(str(id_entitate), titlu,
                                str(an_aparitie), pret, program)
                    self.__film_validator.valideaza(film)
                    self.__film_repository.adauga(film)
                    numar_filme = numar_filme - 1
                else:
                    list = self.__film_repository.read()
                    if len(list) > 1000:
                        raise Exception("Nu se mai pot adauga filme!")
                    list.clear()
        except Exception:
            return {}

    def cautare_fulltext(self, mesaj):
        """
        Cautare full text
        Parcurge fisierul si unde gaseste mesajul
        il adauga in rezultat
        :return: rezultatul final al cautarii
        """
        rezultat = []
        for film in self.__film_repository.read():
            if mesaj in str(film.id_entitate):
                rezultat.append(str(film.id_entitate))
            if mesaj in str(film.titlu):
                rezultat.append(str(film.titlu))
            if mesaj in str(film.an_aparitie):
                rezultat.append(str(film.an_aparitie))
            if mesaj in str(film.pret):
                rezultat.append(str(film.pret))
            if mesaj in str(film.program):
                rezultat.append(str(film.program))
        return rezultat

    def get_rezervari_film(self):
        """
        Ordoneaza descrescator filmele
        dupa numarul de rezervari
        :return: Lista finala
        """
        rezultat = {}
        for rezervare in self.__rezervare_repository.read():
            id_film = rezervare.id_film_r
            for film in self.__film_repository.read():
                if film.id_entitate == id_film:
                    if film.id_entitate in rezultat.keys():
                        rezultat[film.id_entitate] += 1
                    else:
                        rezultat[film.id_entitate] = 1
                    break
        ordonate = sorted(rezultat.items(), key=lambda x: x[1], reverse=True)
        rezultat_ord = []

        for item in ordonate:
            rezultat_ord.append(item[0])

        rezultat_final = []
        for id in rezultat_ord:
            for film in self.__film_repository.read():
                if id == film.id_entitate:
                    rezultat_final.append(film.titlu)
        return rezultat_final

    def sterge_cascada(self, id_film):
        """
        Sterge toate rezervarile care implica
        entitatea cu id-ul dat
        """
        for film in self.__film_repository.read():
            if str(film.id_entitate) == str(id_film):
                self.sterge(id_film)
                for rezervare in self.__rezervare_repository.read():
                    if str(rezervare.id_film_r) == str(id_film):
                        self.__rezervare_repository.\
                            sterge(rezervare.id_entitate)
