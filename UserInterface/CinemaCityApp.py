import tkinter as tk
from tkinter import ttk

from Domain.user import User


class CinemaCity:
    def __init__(self, master, user):
        self.master = master
        self.master.title("Cinema City")
        self.master.geometry("320x480")


        self.user = user

        # Create a label for the search bar
        self.search_label = ttk.Label(self.master, text="Search", font=("Helvetica", 14),
                                      foreground='white')
        self.search_label.pack(pady=20)

        # Create a search bar
        self.search_entry = ttk.Entry(self.master, font=("Helvetica", 14))
        self.search_entry.pack(fill='x', padx=20, pady=5)

        # Create a search button
        self.search_button = ttk.Button(self.master, text="Search", command=self.search_movies, style="Normal.TButton")
        self.search_button.pack(fill='x', padx=20, pady=10)


        # Create a frame for the buttons
        self.button_frame = ttk.Frame(self.master)

        self.button_frame.pack(fill='x', padx=20, pady=10)

        # Create the admin panel button
        self.admin_button = ttk.Button(self.button_frame, text="Admin Panel", command=self.admin_panel,
                                       style="Big.TButton")
        self.admin_button.pack(side='top', fill='x', pady=5)

        # Create the movies button
        self.movies_button = ttk.Button(self.button_frame, text="Movies", command=self.movies, style="Big.TButton")
        self.movies_button.pack(side='top', fill='x', pady=5)

        # Create the reservations button
        self.reservations_button = ttk.Button(self.button_frame, text="Reservations", command=self.reservations,
                                              style="Big.TButton")
        self.reservations_button.pack(side='top', fill='x', pady=5)

        # Create the fidelity cards button
        self.fidelity_button = ttk.Button(self.button_frame, text="Fidelity Cards", command=self.fidelity_cards,
                                          style="Big.TButton")
        self.fidelity_button.pack(side='top', fill='x', pady=5)

    def search_movies(self):
        query = self.search_entry.get()
        # Code for searching movies goes here

    def admin_panel(self):
        # Code for admin panel goes here
        pass

    def movies(self):
        # Code for movies page goes here
        pass

    def reservations(self):
        # Code for reservations page goes here
        pass

    def fidelity_cards(self):
        # Code for fidelity cards page goes here
        pass



