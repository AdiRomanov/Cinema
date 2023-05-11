from dataclasses import dataclass


@dataclass
class FilmError(Exception):
    mesaj: any

    def __str__(self):
        return f'FilmError: {self.mesaj}'


@dataclass
class CardError(Exception):
    mesaj: any

    def __str__(self):
        return f'CardError: {self.mesaj}'


@dataclass
class RezervareError(Exception):
    mesaj: any

    def __str__(self):
        return f'RezervareError: {self.mesaj}'

@dataclass
class UserError(Exception):
    mesaj: any

    def __str__(self):
        return f'UserError: {self.mesaj}'
