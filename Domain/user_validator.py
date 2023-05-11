from Domain.film import Film
from Domain.errors import FilmError, UserError
from Domain.user import User


class UserValidator:
    """
    Valideaza un user.
    """
    @staticmethod
    def valideaza(user: User):
        """
        Valideaza un user
        """
        err = []
        if int(user.id_entitate) < 1:
            err.append("Id-ul este invalid! ")
        if user.username == '':
            err.append("Username-ul este invalid! ")
        if user.email == '':
            err.append("Email-ul este invalid! ")
        if user.password == '':
            err.append("Parola este invalida! ")

        if len(err) > 0:
            raise UserError(err)
