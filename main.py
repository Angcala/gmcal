from scheduling.calendar import Calendar
from scheduling.member import MemberService
from scheduling.session import Session

from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository

def main():
    # standup the db's
    user_repo = UserRepository('users.json')
    session_repo = SessionRepository('sessions.json')
    
    # TODO: wire up scheduling services for sessions and repository
    member_service = MemberService(user_repo)
    me = member_service.create("TOM")

    cal = Calendar(me)

    print(cal.list_sessions())

if __name__ == "__main__":
    main()
