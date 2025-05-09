from tinydb import TinyDB, Query

from scheduling.member import Member

class UserRepository:
    """
    Repository for interacting with the user data in the database
    """

    def __init__(self, db_name: str):
        self.__db = TinyDB(db_name)

    def save(self, data: Member):
        self.__db.insert(data.to_dict())

    def get_by_name(self, name: str) -> Member:
        User = Query()
        user_obj = self.__db.search(User.name == name)
        return Member(user_obj.name, id=user_obj.id)

