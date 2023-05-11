from Service.card_client_service import CardService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Service.user_service import UserService
from UserInterface.CinemaCityApp import CinemaCity
from UserInterface.login_register_page import LoginRegisterPage
import tkinter as tk
from tkinter import ttk


class Consola:
    def __init__(self, film_service: FilmService,
                 card_service: CardService,
                 rezervare_service: RezervareService,
                 user_service: UserService,
                 undo_redo_service: UndoRedoService):

        self.__film_service = film_service
        self.__card_service = card_service
        self.__rezervare_service = rezervare_service
        self.__user_service = user_service
        self.__undo_redo_service = undo_redo_service

    def run_gui(self):

        app = LoginRegisterPage()
        app.mainloop()
        user_username_or_email = app.get_credentials()
        user = self.__user_service.get_by_username(user_username_or_email)
        if user is None:
            user = self.__user_service.get_by_email(user_username_or_email)

        # print(user)

        if user is not None:
            cinema_app = CinemaCity(tk.Toplevel(), user)
            cinema_app.master.mainloop()

    def run_menu(self):
        while True:
            print("1. CRUD Filme.")
            print("2. CRUD Card Client.")
            print("3. CRUD Rezervare.")
            print("4. Cautare full text")
            print("5. Afiseaza rezervarile dintr-un interval dat.")
            print("6. Afiseaza descrescator filmele dupa nr de rezervari.")
            print("7. Afiseaza cardurile descresc dupa puncte.")
            print("8. Sterge rezervarile dintr-un interval de zile.")
            print("9. Incrementarea cu o valoare data a"
                  " cardurilor a caror zi de nastere"
                  " se afla intr-un interval dat.")
            print("10. Stergere cascada film.")
            print("u. Undo.")
            print("r. Redo.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == '1':
                self.run_meniu_crud_filme()
            elif optiune == '2':
                self.run_meniu_crud_card_client()
            elif optiune == '3':
                self.run_meniu_crud_rezervare()
            elif optiune == '4':
                mesaj = input("Search: ")
                self.ui_cautare_fulltext(mesaj)
            elif optiune == '5':
                self.ui_get_rez_din_interval()
            elif optiune == '6':
                self.ui_get_filme_ordonate()
            elif optiune == '7':
                self.ui_get_card_ord()
            elif optiune == '8':
                self.ui_del_rez_interval()
            elif optiune == '9':
                self.ui_incrementeaza()
            elif optiune == '10':
                self.ui_sterge_cascada()
            elif optiune == 'u':
                self.__undo_redo_service.undo()
            elif optiune == 'r':
                self.__undo_redo_service.redo()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida! Reincercati!")

    def run_meniu_crud_filme(self):
        while True:
            print("1. Adauga film")
            print("2. Sterge film")
            print("3. Modifica film")
            print("a. Afiseaza toate filmele")
            print("g. Genereaza filme")
            print("x. Iesire")

            optiune = input("Dati optiunea: ")

            if optiune == '1':
                self.ui_adauga_film()
            elif optiune == '2':
                self.ui_sterge_film()
            elif optiune == '3':
                self.ui_modifica_film()
            elif optiune == 'a':
                self.ui_show_all_filme()
            elif optiune == 'g':
                self.ui_generate_filme()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida! Reincercati!")

    def ui_adauga_film(self):
        try:
            id_film = input("Dati id-ul filmului: ")
            titlu = input("Dati titlul filmului: ")
            an_aparitie = input("Dati anul aparitiei: ")
            pret = float(input("Dati pretul: "))
            ora1 = input("Dati ora inceperii separata prin ':': ")
            ora2 = input("Dati ora finala separata prin ':': ")

            program = ora1 + "-" + ora2

            self.__film_service.adauga(id_film, titlu,
                                       an_aparitie, pret,
                                       program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_sterge_film(self):
        try:
            id_film = input("Dati id-ul filmului de sters: ")

            self.__film_service.sterge(id_film)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_modifica_film(self):
        try:
            id_film = input("Dati id-ul filmului de modificat: ")
            titlu = input("Dati titlul nou al filmului: ")
            an_aparitie = input("Dati noul an al aparitiei filmului: ")
            pret = input("Dati pretul nou: ")
            program = input("Dati programul nou: ")

            self.__film_service.modifica(id_film, titlu,
                                         an_aparitie, pret,
                                         program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_show_all_filme(self):
        for film in self.__film_service.get_all():
            print(film)

    def run_meniu_crud_card_client(self):
        while True:
            print("1. Adauga card")
            print("2. Sterge card")
            print("3. Modifica card")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")

            optiune = input("Dati optiunea: ")

            if optiune == '1':
                self.ui_adauga_card()
            elif optiune == '2':
                self.ui_sterge_card()
            elif optiune == '3':
                self.ui_modifica_card()
            elif optiune == 'a':
                self.ui_show_all_cards()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida! Reincercati!")

    def ui_adauga_card(self):
        try:
            id_card = input("Dati id-ul cardului: ")
            nume = input("Dati numele: ")
            prenume = input("Dati prenumele: ")
            cnp = input("Dati Cnp: ")
            data_n = input("Data nasterii separata prin '.': ")
            data_i = input("Data inregistrarii separata prin '.': ")
            pct = int(input("Dati numarul de puncte: "))

            self.__card_service.adauga(id_card, nume, prenume,
                                       cnp, data_n, data_i, pct)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_sterge_card(self):
        try:
            id_card = input("Dati id-ul cardului de sters: ")

            self.__card_service.sterge(id_card)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_modifica_card(self):
        try:
            id_card = input("Dati id-ul cardului de modificat: ")
            nume = input("Dati numele: ")
            prenume = input("Dati prenumele: ")
            cnp = input("Dati Cnp: ")
            data_n = input("Data nasterii: ")
            data_i = input("Data inregistrarii: ")
            pct = input("Dati numarul de puncte: ")

            self.__card_service.modifica(id_card, nume, prenume,
                                         cnp, data_n, data_i, pct)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_show_all_cards(self):
        for card in self.__card_service.get_all():
            print(card)

    def run_meniu_crud_rezervare(self):
        while True:
            print("1. Adauga rezervare")
            print("2. Sterge rezervare")
            print("3. Modifica rezervare")
            print("a. Afiseaza toate rezervarile")
            print("x. Iesire")

            optiune = input("Dati optiunea: ")

            if optiune == '1':
                self.ui_adauga_rezervare()
            elif optiune == '2':
                self.ui_sterge_rezervare()
            elif optiune == '3':
                self.ui_modifica_rezervare()
            elif optiune == 'a':
                self.ui_show_all_rezervari()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida! Reincercati!")

    def ui_adauga_rezervare(self):
        try:
            id_rezervare = input("Dati id-ul rezervarii: ")
            id_film_r = input("Dati id-ul filmului: ")
            id_card_client = input("Dati id-ul cardului(0-nu exista): ")
            data = input("Dati data separata prin '.': ")
            ora = input("Data ora separata prin ':': ")

            self.__rezervare_service.adauga(id_rezervare, id_film_r,
                                            id_card_client, data, ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_sterge_rezervare(self):
        try:
            id_rezervare = input("Dati id-ul rezervarii de sters: ")

            self.__rezervare_service.sterge(id_rezervare)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_modifica_rezervare(self):
        try:
            id_rezervare = input("Dati id-ul rezervarii de schimbat: ")
            id_film_r = input("Dati id-ul filmului: ")
            id_card_client = input("Dati id-ul cardului(0 daca nu exista): ")
            data = input("Dati data: ")
            ora = input("Data ora: ")

            self.__rezervare_service.modifica(id_rezervare, id_film_r,
                                              id_card_client, data, ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as ex:
            print(ex)

    def ui_show_all_rezervari(self):
        for rezervare in self.__rezervare_service.get_all():
            print(rezervare)

    def ui_generate_filme(self):
        numar_filme = int(input("Dati numarul de filme ce se vor genera: "))
        self.__film_service.film_random(numar_filme)

    def ui_get_rez_din_interval(self):
        try:
            ora1 = input("Dati ora inceperii(HH:MM): ")
            ora2 = input("Dati ora finala(HH:MM): ")
            rezervari = self.__rezervare_service.raport_a(ora1, ora2)
            for rezervare in rezervari:
                print(rezervare)
        except Exception as e:
            print(e)

    def ui_get_filme_ordonate(self):
        lista = self.__film_service.get_rezervari_film()
        for item in lista:
            print(item)

    def ui_cautare_fulltext(self, mesaj):
        print("Cautare full text clienti: ")
        print(self.__card_service.cautare_fulltext(mesaj))
        print("Cautare full text filme: ")
        print(self.__film_service.cautare_fulltext(mesaj))

    def ui_get_card_ord(self):
        lista = self.__card_service.get_card_ord()
        for item in lista:
            print(item)

    def ui_del_rez_interval(self):
        try:
            data1 = input("Dati prima data(DD.MM.YYYY): ")
            data2 = input("Dati a doua data(DD.MM.YYYY): ")
            if self.validare_data(data1) is True \
                    and self.validare_data(data2) is True:
                self.__rezervare_service. \
                    stergere_rez_interval(data1, data2)
            else:
                print("Datele introduse nu sunt valide.")
        except Exception as e:
            print(e)

    @staticmethod
    def validare_data(data):
        """
        Valideaza data
        :return:
        """
        err = []
        list = data.split(".")

        if int(list[0]) < 1 or int(list[0]) > 31:
            err.append("Data invalida!")
        elif int(list[1]) < 1 or int(list[1]) > 12:
            err.append("Data invalida!")
        elif int(list[2]) < 1900 or int(list[2]) > 2021:
            err.append("Data invalida!")

        if len(err) > 0:
            raise KeyError(err)
        return True

    def ui_incrementeaza(self):
        try:
            data1 = input("Dati prima data(DD.MM.YYYY): ")
            data2 = input("Dati a doua data(DD.MM.YYYY): ")
            puncte = input("Dati numarul de puncte: ")
            if self.validare_data(data1) is True \
                    and self.validare_data(data2) is True:
                self.__card_service.incrementare(data1, data2, puncte)
            else:
                print("Datele introduse nu sunt valide.")
        except Exception as e:
            print(e)

    def ui_sterge_cascada(self):
        try:
            id_film = input("Dati id-ul filmului: ")
            self.__film_service.sterge_cascada(id_film)
        except Exception as e:
            print(e)
