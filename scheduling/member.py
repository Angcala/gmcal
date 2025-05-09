from uuid import uuid4


class Member:
    def __init__(self, name: str, id: str=None):
        self._id = id if id else str(uuid4())
        self.name = name

    def to_dict(self) -> dict:
        return {"id": self._id, "name": self.name}


class MemberService:
    def __init__(self, user_repo):
        self.__repo = user_repo

    def create(self, name: str) -> Member:
        member = Member(name)
        self.__repo.save(member)
        return member

    def get_by_name(self, name: str) -> Member:
        return self.__repo.get_by_name(name)

