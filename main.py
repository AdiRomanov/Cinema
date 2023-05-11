from Domain.card_client_validator import CardValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Domain.user_validator import UserValidator
from Repository.repository_json import RepositoryJson
from Service.card_client_service import CardService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Service.user_service import UserService
from Test.tests import Test
from UserInterface.consola import Consola


def main():

    undo_redo_service = UndoRedoService()
    film_repository_json = RepositoryJson("Resources/filme.json")
    film_validator = FilmValidator()
    film_service = FilmService(film_repository_json, film_validator,
                               RepositoryJson("Resources/rezervari.json"),
                               undo_redo_service)

    card_repository_json = RepositoryJson("Resources/carduri.json")
    card_client_validator = CardValidator()
    card_service = CardService(card_repository_json, card_client_validator,
                               undo_redo_service)

    rezervare_repository_json = RepositoryJson("Resources/rezervari.json")
    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(rezervare_repository_json,
                                         rezervare_validator,
                                         undo_redo_service)

    user_repository_json = RepositoryJson("Resources/users.json")
    user_validator = UserValidator()
    user_service = UserService(user_repository_json, user_validator)

    consola = Consola(film_service, card_service, rezervare_service, user_service,
                      undo_redo_service)
    test = Test()
    test.run_all_test()
    # consola.run_menu()
    consola.run_gui()


if __name__ == '__main__':
    main()
