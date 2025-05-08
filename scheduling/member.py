from uuid import uuid4

from .response import Response
from .session import Session

class Member:
    def __init__(self, name: str, sessions: List[Session], id: str=None):
        self._id = id if id else str(uuid4())
        self.name = name
        self._sessions = sessions

    def respond_to_session(self, session_id: str, response: Response):
        # update the session if it exists, otherwise add it
        self._sessions[session_id] = response

    def to_dict(self) -> dict:
        return {id: self._id, name: self.name, sessions: self._sessions}

