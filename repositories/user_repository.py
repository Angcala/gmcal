from tinydb import TinyDB, Query

from typing import List

from scheduling.member import Member

class UserRepository:
    """
    Repository for interacting with the user data in the database
    """

    def __init__(self, db_name: str):
        self.__db = TinyDB(db_name)

    def save(self, data: Member):
        user_obj = data.to_dict()
        user_obj["name"] = user_obj["name"].lower()
        self.__db.insert(user_obj)

    def get_all_users(self) -> List[Member]:
        return self.__db.all()

    def get_by_name(self, name: str) -> Member:
        User = Query()
        user_list = self.__db.search(User.name == name.lower())
        # just get the first match for now
        user_obj = user_list[0]
        return Member(user_obj["name"], id=user_obj["id"])

