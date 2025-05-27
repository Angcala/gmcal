from tinydb import TinyDB, Query, where

from typing import List
from datetime import datetime

from scheduling.session import Session
from scheduling.member import Member
from scheduling.response import Proposal

class SessionRepository:
    """
    Repository for interacting with the database's session objects
    """

    def __init__(self, db_name: str):
        self.__db = TinyDB(db_name)

    def delete(self, session_id: str):
        SessionQ = Query()
        self.__db.remove(SessionQ.id == session_id)

    def save(self, session_data: Session):
        self.__db.insert(session_data.to_dict())

    def get_by_id(self, id: str) -> Session:
        SessionQ = Query()
        session_obj = self.__db.search(SessionQ.id == id)
        obj = session_obj[0]
        creator = Member(obj["creator"]["name"], id=obj["creator"]["id"])
        time = Proposal(datetime.strptime(obj["date"]["start"], "%Y-%m-%dT%H:%M:%S"), datetime.strptime(obj["date"]["end"], "%Y-%m-%dT%H:%M:%S"), creator)
        members = []
        for mem in obj["members"]:
            members.append(Member(mem["name"], id=mem["id"]))

        return Session(creator, time, members, id=obj["id"])

    def get_by_user(self, name: str) -> List[Session]:
        sessions = []
        session_objs = self.__db.search(where('creator').name == name)
        for obj in session_objs:
            sesh = Session(obj["creator"], obj["date"], obj["members"], id=obj["id"])
            sessions.append(sesh)
        return list(sessions)

