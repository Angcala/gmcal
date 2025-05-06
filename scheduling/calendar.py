from typing import List

from .session import Session
from .member import Member

class Calendar:
    """a calendar is a collection of sessions"""
    def __init__(self, created_by: Member):
        self._created_by = created_by
        self.sessions: List(Session) = []

    def add_session(self, session: Session) -> None:
        self.sessions.append(session)

    def list_sessions(self):
        return self.sessions
