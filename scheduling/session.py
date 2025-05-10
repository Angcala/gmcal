from datetime import datetime
from typing import List
from uuid import uuid4

from .member import Member
from .response import Response

class Session:
    """A session is just a datetime with a list of members
    The member itself holds whether it is attending or not
    
    """
    def __init__(self, creator: Member, date: datetime, members: List[Member], id: str=None):
        self.id = id if id else str(uuid4()) 
        self.creator = creator
        self.date = date
        self.members = members

    def members_attending(self) -> List[Member]:
        """return members that have responded YES"""
        attending_members = []
        for member in self._members:
            if member.is_attending(self.id):
                attending_members.append(member)

        return attending_members

    def member_responses(self) -> List[Member]:
        # iterate over members and return a map with member: responses
        ...

    def suggested_times(self) -> List[datetime]:
        # return all suggested times from members
        ...

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "creator": self.creator,
            "date": self.date,
            "members": self.members
        }

class SessionService:
    def __init__(self, session_repo):
        self.__repo = session_repo

    def create(self, creator: Member, date: datetime, members: List[Member], id: str=None) -> Session:
        creator = creator.to_dict()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        members = [m.to_dict() for m in members]
        session = Session(creator, date, members, id=id)
        self.__repo.save(session)
        return session

    def get_by_id(self, id: str) -> Session:
        return self.__repo.get_by_id(id)

    def list_users_sessions(self, user: Member) -> List[Session]:
        # get all sessions where user is the creator or member
        # TODO: Right now this only searches sessions you created. 
        # TODO: It should include sessions you are a member of
        
        return self.__repo.get_by_user(user.name)

        
        
