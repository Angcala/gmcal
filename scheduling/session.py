from datetime import datetime
from typing import List
from uuid import uuid4

from .member import Member, MemberService
from .response import Response, Proposal, ProposalService

class Session:
    """A session is just a datetime with a list of members
    The member itself holds whether it is attending or not
    
    """
    def __init__(self, creator: Member, proposed_time: Proposal, members: List[Member], id: str=None):
        self.id = id if id else str(uuid4()) 
        self.creator = creator
        self.proposed_time = proposed_time
        self.members = members
        self.responses = None

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
            "date": self.proposed_time,
            "members": self.members
        }

class SessionService:
    def __init__(self, session_repo, member_svc: MemberService, proposal_svc: ProposalService):
        self.__repo = session_repo
        self.__member_svc = member_svc
        self.__proposal_svc = proposal_svc

    def create(self, creator_name: str, start: datetime, end: datetime, members: List[str], id: str=None) -> Session:

        try:
            creator = self.__member_svc.get_by_name(creator_name)
        except Exception as e:
            raise ValueError(f"creator {creator_name} not found! ", e)


        proposed_time = self.__proposal_svc.make_new_proposal(start, end, creator.name)

        players = []
        for player in members:
            try:
                user = self.__member_svc.get_by_name(player)
            except Exception as e:
                raise ValueError(f"user {player} not found! ", e)

            players.append(user)


        session = Session(creator, proposed_time, players, id=id)
        self.__repo.save(session)
        return session


    def get_by_id(self, id: str) -> Session:
        return self.__repo.get_by_id(id)

    def list_users_sessions(self, user: Member) -> List[Session]:
        # get all sessions where user is the creator or member
        # TODO: Right now this only searches sessions you created. 
        # TODO: It should include sessions you are a member of
        
        return self.__repo.get_by_user(user.name)

        
        
