from Domain.entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiect_adaugat: Entitate):
        self.repository = repository
        self.obiect_adaugat = obiect_adaugat

    def do_undo(self):
        self.repository.sterge(self.obiect_adaugat.id_entitate)

    def do_redo(self):
        self.repository.adauga(self.obiect_adaugat)
