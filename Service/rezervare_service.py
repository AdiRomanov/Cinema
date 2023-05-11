import datetime

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator

from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class RezervareService:
    def __init__(self, rezervare_repository: Repository,
                 rezervare_validator: RezervareValidator,
                 undo_redo_service: UndoRedoService = None):
        self.__rezervare_repository = rezervare_repository
        self.__rezervare_validator = rezervare_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        :return: O lista de rezervari
        """
        return self.__rezervare_repository.read()

    def adauga(self, id_rezervare, id_film_r, id_card_client, data, ora):
        """
        Adauga o rezervare in lista
        """
        rezervare = Rezervare(id_rezervare, id_film_r,
                              id_card_client, data, ora)
        self.__rezervare_validator.valideaza(rezervare)
        self.__rezervare_repository.adauga(rezervare)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service.add_undo_operation(
                AddOperation(self.__rezervare_repository, rezervare))

    def sterge(self, id_entitate):
        """
        Sterge o rezervare din lista
        """
        rezervare = self.__rezervare_repository.read(id_entitate)
        self.__rezervare_repository.sterge(id_entitate)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service. \
                add_undo_operation(DeleteOperation
                                   (self.__rezervare_repository,
                                    rezervare))

    def modifica(self, id_entitate, id_film_r, id_card_client, data, ora):
        """
        Modifica o rezervare din lista
        """
        rezervare_ant = self.__rezervare_repository.read(id_entitate)
        rezervare = Rezervare(id_entitate, id_film_r,
                              id_card_client, data, ora)
        self.__rezervare_validator.valideaza(rezervare)
        self.__rezervare_repository.modifica(rezervare)
        if self.__undo_redo_service is not None:
            self.__undo_redo_service. \
                add_undo_operation(ModifyOperation
                                   (self.__rezervare_repository,
                                    rezervare,
                                    rezervare_ant))

    def raport_a(self, ora1, ora2):
        """
        Returneaza toate rezervarile dintr-un interval orar dat
        """
        rezervari = self.__rezervare_repository.read()
        try:

            interval = ora1 + " - " + ora2
            err = []
            list = interval.split("-")
            st = list[0].split(":")
            dr = list[1].split(":")
            if int(st[0]) < 0 or int(st[0]) > 23 \
                    or int(st[1]) < 0 or int(st[1]) > 59:
                err.append("Ora inceperii este invalida! ")
            if int(dr[0]) < 0 or int(dr[0]) > 23 \
                    or int(dr[1]) < 0 or int(dr[1]) > 59:
                err.append("Ora finala este invalida! ")
            if len(err) > 0:
                raise err
            rezultat = []
            for rezervare in rezervari:
                ora = rezervare.ora.split(":")
                if st[0] < ora[0] < dr[0]:
                    rezultat.append(rezervare)
                elif ora[0] == st[0] and ora[1] >= st[1]:
                    rezultat.append(rezervare)
                elif ora[0] == dr[0] and ora[1] <= dr[1]:
                    rezultat.append(rezervare)
            return rezultat
        except Exception as ex:
            print(ex)

    def stergere_rez_interval(self, data1, data2):
        """
        Sterge rezervari dintr-un interval dat
        """
        string1 = data1.split('.')
        string2 = data2.split('.')
        start = datetime.datetime(int(string1[2]),
                                  int(string1[1]),
                                  int(string1[0]))
        end = datetime.datetime(int(string2[2]),
                                int(string2[1]),
                                int(string2[0]))
        for rezervare in self.__rezervare_repository.read():
            string3 = rezervare.data
            string = string3.split('.')
            data = datetime.datetime(int(string[2]),
                                     int(string[1]),
                                     int(string[0]))
            if start <= data <= end:
                self.__rezervare_repository.sterge(rezervare.id_entitate)
