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
        self._id = id if id else str(uuid4()) 
        self._creator = creator
        self._date = date
        self._members = members

    def members_attending(self) -> List[Member]:
        """return members that have responded YES"""
        attending_members = []
        for member in self._members:
            if member.is_attending(self._id):
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
            id: self._id,
            creator: self._creator,
            date: self._date,
            members: self._members
        }

