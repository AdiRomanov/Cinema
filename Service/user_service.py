import random
import string

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.user_validator import UserValidator
from Domain.modify_operation import ModifyOperation
from Domain.user import User
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class UserService:
    def __init__(self, user_repository: Repository,
                 user_validator: UserValidator,
                 rezervare_repository: Repository = None,
                 undo_redo_service: UndoRedoService = None):
        self.__user_repository = user_repository
        self.__user_validator = user_validator

    def get_all(self):
        """
        :return: Lista de filme
        """
        return self.__user_repository.read()

    def adauga(self, username, email, password):
        """
        Adauga un film in lista
        """
        id_entitate = random.randint(1, 1000)
        while self.__user_repository.read(id_entitate) is not None:
            id_entitate = random.randint(1, 1000)

        user = User(id_entitate, username, email, password)
        self.__user_validator.valideaza(user)
        self.__user_repository.adauga(user)

    def sterge(self, id_entitate):
        """
        Sterge un film din lista
        """
        user = self.__user_repository.read(id_entitate)
        self.__user_repository.sterge(id_entitate)

    def modifica(self, id_entitate, username, email, password):
        """
        Modifica un film din lista
        """
        user_anterior = self.__user_repository.read(id_entitate)
        user = User(id_entitate, username, email, password)
        if user_anterior == user:
            self.__user_validator.valideaza(user)
            self.__user_repository.modifica(user)

    def get_by_username(self, searched_username):

        for user in self.__user_repository.read():
            if user.username == searched_username:
                return user

        return None

    def get_by_email(self, searched_email):

        for user in self.__user_repository.read():
            if user.email == searched_email:
                return user

        return None
