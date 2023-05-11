from Domain.card_client import Card
from Domain.card_client_validator import CardValidator
from Domain.entitate import Entitate
from Domain.errors import FilmError
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.repository_in_memory import RepositoryInMemory
from Repository.repository_json import RepositoryJson
from Service.card_client_service import CardService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


class Test(object):

    def run_all_test(self):
        self.__test_film()
        self.__test_film_validator()
        self.__test_card_client()
        self.__test_card_validator()
        self.__test_rezervare()
        self.__test_rezervare_validator()
        self.__test_entitate()
        self.__test_repository_adauga()
        self.__test_repository_read()
        self.__test_repository_sterge()
        self.__test_repository_modifica()
        self.__test_srv_film_adauga()
        self.__test_srv_film_sterge()
        self.__test_srv_get_all()
        self.__test_srv_modifica()
        self.__test_srv_film_random()
        self.__test_srv_fulltext()
        self.__test_raport_a()
        # self.__test_get_filme_ordonate()
        self.__test_get_card_ord()
        self.__test_del_rez_interval()
        self.__test_incrementeaza()
        # self.__test_sterge_cascada()
        self.__test_undo()
        self.__test_redo()

    @staticmethod
    def __test_film():
        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        assert film.id_entitate == id
        assert film.titlu == titlu
        assert film.an_aparitie == an_aparitie
        assert film.pret == pret
        assert film.program == program

    @staticmethod
    def __test_film_validator():
        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        film_validator = FilmValidator
        assert film_validator.valideaza(film) is None

        id = '11'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 10
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        assert film_validator.valideaza(film) is None

    @staticmethod
    def __test_card_client():
        id = '100'
        nume = 'An'
        prenume = 'Sb'
        cnp = '1234567891234'
        data_n = '10.10.2000'
        data_i = '15.10.2010'
        pct = 10
        card = Card(id, nume, prenume, cnp, data_n, data_i, pct)
        assert card.id_entitate == id
        assert card.nume == nume
        assert card.prenume == prenume
        assert card.cnp == cnp
        assert card.data_i == data_i
        assert card.data_n == data_n
        assert card.pct == pct

    @staticmethod
    def __test_card_validator():
        id = '100'
        nume = 'An'
        prenume = 'Sb'
        cnp = '1234567891234'
        data_n = '10.10.2000'
        data_i = '15.10.2010'
        pct = 10
        card = Card(id, nume, prenume, cnp, data_n, data_i, pct)
        card_validator = CardValidator
        assert card_validator.valideaza(card) is None

        id = '13'
        nume = 'faf'
        prenume = 'dsg'
        cnp = '1234567891234'
        data_n = '10.10.2000'
        data_i = '15.10.2010'
        pct = 10
        card = Card(id, nume, prenume, cnp, data_n, data_i, pct)
        assert card_validator.valideaza(card) is None

    @staticmethod
    def __test_rezervare():
        id = '1'
        id_film_r = '100'
        id_card_client = '10'
        data = '10.10.2020'
        ora = '20:30'
        rezervare = Rezervare(id, id_film_r, id_card_client, data, ora)
        assert rezervare.id_entitate == id
        assert rezervare.id_film_r == id_film_r
        assert rezervare.id_card_client == id_card_client
        assert rezervare.data == data
        assert rezervare.ora == ora

    @staticmethod
    def __test_rezervare_validator():
        id = '1'
        id_film_r = '100'
        id_card_client = '10'
        data = '10.10.2020'
        ora = '20:30'
        rezervare = Rezervare(id, id_film_r, id_card_client, data, ora)
        rezervare_validator = RezervareValidator
        assert rezervare_validator.valideaza(rezervare) is None

        id = '2'
        id_film_r = '22'
        id_card_client = '32'
        data = '10.10.2020'
        ora = '20:30'
        rezervare = Rezervare(id, id_film_r, id_card_client, data, ora)
        assert rezervare_validator.valideaza(rezervare) is None

    @staticmethod
    def __test_entitate():
        id = '100'
        entitate = Entitate(id)
        assert entitate.id_entitate == id

    @staticmethod
    def __test_repository_adauga():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()

        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        films = repo.read()
        assert len(films) == 0
        repo.adauga(film)
        films = repo.read()
        assert len(films) == 1
        assert films[0] == film
        assert repo.read(id) == film
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        alt_film = Film(id, alt_titlu, alt_an_aparitie,
                        alt_pret, alt_program)
        try:
            repo.adauga(alt_film)
            assert False
        except KeyError as ke:
            assert str(ke) == "'Exista deja o entitate cu id-ul dat!'"

    @staticmethod
    def __test_repository_read():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        repo.adauga(film)
        alt_id = '11'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        alt_film = Film(alt_id, alt_titlu, alt_an_aparitie,
                        alt_pret, alt_program)
        repo.adauga(alt_film)
        assert repo.read(id) == film
        assert repo.read(alt_id) == alt_film
        films = repo.read()
        assert len(films) == 2
        assert films[0] == film
        assert films[1] == alt_film

    @staticmethod
    def __test_repository_sterge():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)

        films = repo.read()
        assert len(films) == 0
        repo.adauga(film)
        films = repo.read()
        assert len(films) == 1

        alt_id = '11'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        alt_film = Film(alt_id, alt_titlu, alt_an_aparitie,
                        alt_pret, alt_program)
        repo.adauga(alt_film)
        films = repo.read()
        assert len(films) == 2
        repo.sterge(alt_id)
        films = repo.read()
        assert len(films) == 1
        repo.sterge(id)
        films = repo.read()
        assert len(films) == 0

    @staticmethod
    def __test_repository_modifica():
        """filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)"""
        repo = RepositoryInMemory()
        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        film = Film(id, titlu, an_aparitie, pret, program)
        repo.adauga(film)
        films = repo.read()
        assert films[0] == film
        alt_id = '10'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        alt_film = Film(alt_id, alt_titlu, alt_an_aparitie,
                        alt_pret, alt_program)

        repo.modifica(alt_film)
        films = repo.read()
        assert films[0] == alt_film

    @staticmethod
    def __test_srv_film_adauga():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        assert len(film_service.get_all()) == 0
        film_service.adauga(id, titlu, an_aparitie, pret, program)
        assert film_service.get_all()[0].id_entitate == id
        assert film_service.get_all()[0].titlu == titlu
        assert film_service.get_all()[0].an_aparitie == an_aparitie
        assert film_service.get_all()[0].pret == pret
        assert film_service.get_all()[0].program == program
        assert len(film_service.get_all()) == 1

        id_invalid = '-10'
        titlu_invalid = ''
        an_aparitie_invalid = '50000'
        pret_invalid = -10.5
        program_invalid = '45:10 - 35:98'
        try:
            film_service.adauga(id_invalid,
                                titlu_invalid,
                                an_aparitie_invalid,
                                pret_invalid, program_invalid)
            assert False
        except FilmError as fe:
            err = ''
            err += "FilmError: ['Id-ul este invalid! ',"
            err += " 'Titlul este invalid! ', "
            err += "'Pretul nu poate sa fie 0 sau negativ! ', "
            err += "'Anul de aparitie este invalid! ', "
            err += "'Ora inceperii este invalida! ', "
            err += "'Ora finala este invalida! ']"
            assert str(fe) == err

        alt_id = '10'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        try:
            film_service.adauga(alt_id, alt_titlu, alt_an_aparitie,
                                alt_pret, alt_program)
            assert False
        except KeyError as ke:
            assert str(ke) == "'Exista deja o entitate cu id-ul dat!'"

    @staticmethod
    def __test_srv_film_sterge():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        assert len(film_service.get_all()) == 0
        film_service.adauga(id, titlu, an_aparitie, pret, program)
        assert len(film_service.get_all()) == 1
        alt_id = '11'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        film_service.adauga(alt_id, alt_titlu, alt_an_aparitie,
                            alt_pret, alt_program)
        assert len(film_service.get_all()) == 2
        film_service.sterge(alt_id)
        assert len(film_service.get_all()) == 1
        try:
            film_service.sterge(alt_id)
            assert False
        except KeyError as ke:
            assert str(ke) == "'Nu exista entitate cu id-ul dat!'"
        assert len(film_service.get_all()) == 1
        film_service.sterge(id)
        assert len(film_service.get_all()) == 0

    @staticmethod
    def __test_srv_get_all():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        assert len(film_service.get_all()) == 0
        film_service.adauga(id, titlu, an_aparitie, pret, program)
        assert len(film_service.get_all()) == 1
        alt_id = '11'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        film_service.adauga(alt_id, alt_titlu, alt_an_aparitie,
                            alt_pret, alt_program)
        assert len(film_service.get_all()) == 2

    @staticmethod
    def __test_srv_modifica():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        id = '10'
        titlu = 'Pacanele'
        an_aparitie = '2000'
        pret = 20.5
        program = '10:20 - 11:30'
        assert len(film_service.get_all()) == 0
        film_service.adauga(id, titlu, an_aparitie, pret, program)
        assert len(film_service.get_all()) == 1
        alt_id = '10'
        alt_titlu = 'Book of Ra'
        alt_an_aparitie = '1990'
        alt_pret = 100.1
        alt_program = '01:00 - 02:30'
        film_service.modifica(alt_id, alt_titlu,
                              alt_an_aparitie,
                              alt_pret, alt_program)
        assert film_service.get_all()[0].id_entitate == alt_id
        assert film_service.get_all()[0].titlu == alt_titlu
        assert film_service.get_all()[0].an_aparitie == alt_an_aparitie
        assert film_service.get_all()[0].pret == alt_pret
        assert film_service.get_all()[0].program == alt_program

        id_invalid = '20'
        titlu_invalid = 'dsadsa'
        an_aparitie_invalid = '2010'
        pret_invalid = 10.5
        program_invalid = '10:10 - 11:20'
        try:
            film_service.modifica(id_invalid, titlu_invalid,
                                  an_aparitie_invalid,
                                  pret_invalid, program_invalid)
            assert False
        except KeyError as ke:
            assert str(ke) == "'Nu exista entitate cu id-ul dat!'"

    @staticmethod
    def __test_srv_film_random():
        """filename = "teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)"""
        repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)
        assert len(film_service.get_all()) == 0
        film_service.film_random(1)
        assert len(film_service.get_all()) == 1

    @staticmethod
    def __test_raport_a():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        rezervare_validator = RezervareValidator()
        rezervare_service = RezervareService(repo, rezervare_validator)

        rezervare1 = Rezervare('1', '2', '2', '10.10.2020', '10:10')
        rezervare2 = Rezervare('2', '3', '4', '10.11.2020', '15:30')
        rezervare_validator.valideaza(rezervare1)
        rezervare_validator.valideaza(rezervare2)
        repo.adauga(rezervare1)
        repo.adauga(rezervare2)

        list = []
        assert len(list) == 0
        list = rezervare_service.raport_a('10:00', '12:00')
        assert len(list) == 1
        assert list[0] == rezervare1

    @staticmethod
    def __test_srv_fulltext():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        film1 = Film('1', 'F1', "2010", 100, '11:30 - 12:30')
        film2 = Film('2', 'F2', "2020", 1020, '15:45 - 17:00')
        film3 = Film('3', 'F3', "2012", 15, '20:00 - 21:30')

        film_validator.valideaza(film1)
        film_validator.valideaza(film2)
        film_validator.valideaza(film3)

        repo.adauga(film1)
        repo.adauga(film2)
        repo.adauga(film3)

        assert film_service.cautare_fulltext('10') == \
               ['2010', '100', '1020']
        assert film_service.cautare_fulltext('201') == \
               ["2010", "2012"]
        assert film_service.cautare_fulltext('F') == \
               ['F1', 'F2', 'F3']

    @staticmethod
    def __test_get_filme_ordonate():
        repo = RepositoryInMemory()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)
        rezervare_validator = RezervareValidator()
        rezervare_service = RezervareService(repo, rezervare_validator)

        film1 = Film('1', 'F1', "2010", 100, '11:30 - 12:30')
        film2 = Film('2', 'F2', "2020", 1020, '15:45 - 17:00')
        film3 = Film('3', 'F3', "2012", 15, '20:00 - 21:30')
        film_service.adauga('1', 'F1', "2010", 100, '11:30 - 12:30')
        film_service.adauga('2', 'F2', "2020", 1020, '15:45 - 17:00')
        film_service.adauga('3', 'F3', "2012", 15, '20:00 - 21:30')

        rezervare1 = Rezervare('7', '2', '2', '10.10.2020', '10:10')
        rezervare2 = Rezervare('8', '2', '4', '10.11.2020', '15:30')
        rezervare3 = Rezervare('9', '1', '4', '10.12.2020', '16:50')
        rezervare4 = Rezervare('10', '3', '5', '11.12.2020', '19:50')
        rezervare_service.adauga('7', '2', '2', '10.10.2020', '10:10')
        rezervare_service.adauga('8', '2', '4', '10.11.2020', '15:30')
        rezervare_service.adauga('9', '1', '4', '10.12.2020', '16:50')
        rezervare_service.adauga('10', '3', '5', '11.12.2020', '19:50')

        lista = []
        assert len(lista) == 0
        lista = film_service.get_rezervari_film()
        print(lista)
        assert len(lista) == 3
        assert lista[0] == film2
        assert lista[1] == film1
        assert lista[2] == film3

    @staticmethod
    def __test_get_card_ord():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        # repo = RepositoryInMemory()
        card_validator = CardValidator()
        card_service = CardService(repo, card_validator)

        card1 = Card('1', 'da', 'nu', '5020404244488', '10.10.1990',
                     '10.11.2003', 100)
        card2 = Card('2', 'das', 'nus', '5020404244488', '10.10.1989',
                     '10.11.2010', 600)

        repo.adauga(card1)
        repo.adauga(card2)
        lista = []
        assert len(lista) == 0
        lista = card_service.get_card_ord()
        assert len(lista) == 2
        assert lista[0] == card2
        assert lista[1] == card1

    @staticmethod
    def __test_del_rez_interval():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)

        rezervare_validator = RezervareValidator()
        rezervare_service = RezervareService(repo, rezervare_validator)

        rezervare1 = Rezervare('7', '2', '2', '10.10.2020', '10:10')
        rezervare2 = Rezervare('8', '2', '4', '10.11.2019', '15:30')
        rezervare3 = Rezervare('9', '1', '4', '10.12.2018', '16:50')
        rezervare4 = Rezervare('10', '3', '5', '11.12.2017', '19:50')

        repo.adauga(rezervare1)
        repo.adauga(rezervare2)
        repo.adauga(rezervare3)
        repo.adauga(rezervare4)

        list = repo.read()
        assert len(list) == 4
        rezervare_service.stergere_rez_interval('10.10.2019', '10.12.2021')
        list = repo.read()
        assert len(list) == 2
        assert list[0] == rezervare3
        assert list[1] == rezervare4

    @staticmethod
    def __test_incrementeaza():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)

        card_validator = CardValidator()
        card_service = CardService(repo, card_validator)

        card1 = Card('1', 'da', 'nu', '5020404244488', '10.10.2000',
                     '10.11.2003', 100)
        card2 = Card('2', 'das', 'nus', '5020404244488', '10.10.1989',
                     '10.11.2010', 600)

        repo.adauga(card1)
        repo.adauga(card2)
        lista = []
        assert len(lista) == 0
        lista = card_service.get_all()
        assert len(lista) == 2
        card_service.incrementare('10.10.1990', '10.10.2001', 300)
        lista = card_service.get_all()
        assert lista[0].pct == 400

    @staticmethod
    def __test_sterge_cascada():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)

        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator)

        rezervare_validator = RezervareValidator()
        rezervare_service = RezervareService(repo, rezervare_validator)

        film1 = Film('1', 'F1', "2010", 100, '11:30 - 12:30')
        film2 = Film('2', 'F2', "2020", 1020, '15:45 - 17:00')
        film3 = Film('3', 'F3', "2012", 15, '20:00 - 21:30')
        repo.adauga(film1)
        repo.adauga(film2)
        repo.adauga(film3)

        rezervare1 = Rezervare('7', '2', '2', '10.10.2020', '10:10')
        rezervare2 = Rezervare('8', '2', '4', '10.11.2020', '15:30')
        rezervare3 = Rezervare('9', '1', '4', '10.12.2020', '16:50')
        rezervare4 = Rezervare('10', '3', '5', '11.12.2020', '19:50')
        repo.adauga(rezervare1)
        repo.adauga(rezervare2)
        repo.adauga(rezervare3)
        repo.adauga(rezervare4)

        entitati = repo.read()
        film_service.sterge_cascada('2')

    @staticmethod
    def __test_undo():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        undo_redo_service = UndoRedoService()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator,
                                   RepositoryJson("Resources/teste.json"),
                                   undo_redo_service)

        film_service.adauga('1', 'F1', "2010", 100, '11:30 - 12:30')
        film_service.adauga('2', 'F2', "2020", 1020, '15:45 - 17:00')
        filme = film_service.get_all()
        assert len(filme) == 2
        undo_redo_service.undo()
        filme = film_service.get_all()
        assert len(filme) == 1
        undo_redo_service.undo()
        filme = film_service.get_all()
        assert len(filme) == 0

    @staticmethod
    def __test_redo():
        filename = "Resources/teste.json"
        with open(filename, 'w') as f:
            f.write("")
        repo = RepositoryJson(filename)
        undo_redo_service = UndoRedoService()
        film_validator = FilmValidator()
        film_service = FilmService(repo, film_validator,
                                   RepositoryJson("../Resources/teste.json"),
                                   undo_redo_service)

        film_service.adauga('1', 'F1', "2010", 100, '11:30 - 12:30')
        film_service.adauga('2', 'F2', "2020", 1020, '15:45 - 17:00')
        filme = film_service.get_all()
        assert len(filme) == 2
        undo_redo_service.undo()
        filme = film_service.get_all()
        assert len(filme) == 1
        undo_redo_service.undo()
        filme = film_service.get_all()
        assert len(filme) == 0
        undo_redo_service.redo()
        filme = film_service.get_all()
        assert len(filme) == 1
        undo_redo_service.redo()
        filme = film_service.get_all()
        assert len(filme) == 2
