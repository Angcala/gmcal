from tinydb import TinyDB, Query, where

from typing import List

from scheduling.session import Session

class SessionRepository:
    """
    Repository for interacting with the database's session objects
    """

    def __init__(self, db_name: str):
        self.__db = TinyDB(db_name)

    def save(self, session_data: Session):
        self.__db.insert(session_data.to_dict())

    def get_by_id(self, id: str) -> Session:
        Session = Query()
        session_obj = self.__db.search(Session.id == id)
        return Session(session_obj.creator, session_obj.date, session_obj.members, id=session_obj.id)

    def get_by_user(self, name: str) -> List[Session]:
        sessions = []
        session_objs = self.__db.search(where('creator').name == name)
        for obj in session_objs:
            sesh = Session(obj["creator"], obj["date"], obj["members"], id=obj["id"])
            sessions.append(sesh)
        return list(sessions)

