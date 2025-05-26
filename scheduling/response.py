from enum import Enum
from datetime import datetime

from scheduling.member import Member, MemberService

class Proposal:
    def __init__(self, start: datetime, end: datetime, user: Member):
        self.start = start
        self.end = end
        self.creator = user
    
    def to_dict(self) -> dict:
        return {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "creator": self.creator.to_dict()
        }



class Response(Enum):
    YES: str = "yes"
    NO: str = "no"
    PROPOSAL: Proposal = None

    suggested_time: datetime | None = None

    @classmethod
    def set_suggested_time(cls, new_time: datetime):
        cls.suggested_time = new_time


class ProposalService:
    def __init__(self, member_svc: MemberService):
        self.__member_svc = member_svc
    
    def make_new_proposal(self, start: datetime, end: datetime, username: str) -> Proposal:
        try:
            creator = self.__member_svc.get_by_name(username)
        except Exception as e:
            raise ValueError(f"user {username} not found! ", e)

        return Proposal(start, end, creator)
