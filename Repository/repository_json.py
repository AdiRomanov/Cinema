import jsonpickle

from Domain.entitate import Entitate
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        """
        Returneaza lista de entitati daca id_entitate este None
        Returneaza entitatea cu id-ul specificat, daca exista
        """
        self.entitati = self.__read_file()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate):
        """
        Adauga o entitate in lista
        :param entitate: entitatea adaugata
        """
        self.entitati = self.__read_file()
        super().adauga(entitate)
        self.__write_file()

    def sterge(self, id_entitate):
        """
        Sterge o entitate cu id-ul specificat din lista
        :param id_entitate: id-ul entitatii
        """
        self.entitati = self.__read_file()
        super().sterge(id_entitate)
        self.__write_file()

    def modifica(self, entitate: Entitate):
        """
        Modifica o entitate cu id-ul specificat din lista
        :param entitate: entitatea noua
        """
        self.entitati = self.__read_file()
        super().modifica(entitate)
        self.__write_file()
