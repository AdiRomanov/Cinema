from Domain.entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class ModifyOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiect_modificat: Entitate,
                 obiect_initial: Entitate):
        self.__repository = repository
        self.__obiect_modificat = obiect_modificat
        self.__obiect_initial = obiect_initial

    def do_undo(self):
        self.__repository.modifica(self.__obiect_initial)

    def do_redo(self):
        self.__repository.modifica(self.__obiect_modificat)
