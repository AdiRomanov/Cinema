from Domain.entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Returneaza lista de entitati daca id_entitate este None
        Returneaza entitatea cu id-ul specificat, daca exista
        """
        if id_entitate is None:
            return list(self.entitati.values())

        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga o entitate in lista
        :param entitate: entitatea adaugata
        """
        if self.read(entitate.id_entitate) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate: str):
        """
        Sterge o entitate cu id-ul specificat din lista
        :param id_entitate: id-ul entitatii
        """
        if self.read(id_entitate) is None:
            raise KeyError("Nu exista entitate cu id-ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica o entitate cu id-ul specificat din lista
        :param entitate: entitatea noua
        """
        if self.read(entitate.id_entitate) is None:
            raise KeyError("Nu exista entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate
