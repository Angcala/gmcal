from uuid import uuid4

from response import Response


class Member:
    def __init__(self, name: str):
        self._id = str(uuid4())
        self.name = name
        self._sessions = []

    def respond_to_session(self, session_id: str, response: Response):
        # update the session if it exists, otherwise add it
        self._sessions[session_id] = response

