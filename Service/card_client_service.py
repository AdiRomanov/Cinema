import datetime

from Domain.add_operation import AddOperation
from Domain.card_client import Card
from Domain.card_client_validator import CardValidator
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class CardService:
    def __init__(self, card_repository: Repository,
                 card_validator: CardValidator,
                 undo_redo_service: UndoRedoService = None):
        self.__card_repository = card_repository
        self.__card_validator = card_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        :return: O lista de carduri de fidelitate
        """
        return self.__card_repository.read()

    def adauga(self, id_card, nume, prenume, cnp, data_n, data_i, pct):
        """
        Adauga un card in lista
        """
        card = Card(id_card, nume, prenume, cnp, data_n, data_i, pct)
        self.__card_validator.valideaza(card)
        self.__card_repository.adauga(card)
        self.__undo_redo_service.add_undo_operation(
            AddOperation(self.__card_repository, card))

    def sterge(self, id_entitate):
        """
        Sterge un card din lista
        """
        card = self.__card_repository.read(id_entitate)
        self.__card_repository.sterge(id_entitate)
        self.__undo_redo_service.add_undo_operation(DeleteOperation
                                                    (self.__card_repository,
                                                     card))

    def modifica(self, id_entitate, nume, prenume, cnp, data_n, data_i, pct):
        """
        Modifica un card din lista
        """
        card_anterior = self.__card_repository.read(id_entitate)
        card = Card(id_entitate, nume, prenume, cnp, data_n, data_i, pct)
        self.__card_validator.valideaza(card)
        self.__card_repository.modifica(card)
        self.__undo_redo_service.add_undo_operation(ModifyOperation
                                                    (self.__card_repository,
                                                     card,
                                                     card_anterior))

    def cautare_fulltext(self, mesaj):
        """
        Cautare full text
        Parcurge fisierul si unde gaseste mesajul
        il adauga in rezultat
        :return: rezultatul final al cautarii
        """
        rezultat = []
        for card in self.__card_repository.read():
            if mesaj in str(card.id_entitate):
                rezultat.append(str(card.id_entitate))
            if mesaj in str(card.cnp):
                rezultat.append(str(card.cnp))
            if mesaj in str(card.data_n):
                rezultat.append(str(card.data_n))
            if mesaj in str(card.data_i):
                rezultat.append(str(card.data_i))
            if mesaj in str(card.nume):
                rezultat.append(str(card.nume))
            if mesaj in str(card.prenume):
                rezultat.append(str(card.prenume))
            if mesaj in str(card.puncte):
                rezultat.append(str(card.puncte))
        return rezultat

    def get_card_ord(self):
        """
        Ordoneaza cardurile descrescator
        dupa numarul de puncte
        """
        carduri_ord = []
        lista = []
        for card in self.__card_repository.read():
            carduri_ord.append([card.id_entitate,
                                card.pct])
        rezultat = sorted(carduri_ord,
                          key=lambda x: x[1], reverse=True)
        for rez in rezultat:
            for card in self.__card_repository.read():
                if card.id_entitate == rez[0]:
                    lista.append(card)
        return lista

    def incrementare(self, data1, data2, puncte):
        """
        Incrementeaza cu o valoare data
        punctele de pe cardurile client
        """

        string1 = data1.split('.')
        string2 = data2.split('.')
        start = datetime.datetime(int(string1[2]),
                                  int(string1[1]),
                                  int(string1[0]))
        end = datetime.datetime(int(string2[2]),
                                int(string2[1]),
                                int(string2[0]))
        for card in self.__card_repository.read():
            string3 = card.data_n.split('.')
            data = datetime.datetime(int(string3[2]),
                                     int(string3[1]),
                                     int(string3[0]))
            if start <= data <= end:
                card_nou = Card(card.id_entitate,
                                card.nume,
                                card.prenume,
                                card.cnp,
                                card.data_n,
                                card.data_i,
                                card.pct + int(puncte))
                self.__card_repository.modifica(card_nou)
