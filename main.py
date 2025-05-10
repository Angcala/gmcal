from datetime import datetime

from scheduling.calendar import Calendar
from scheduling.member import MemberService
from scheduling.session import SessionService

from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository

def main():
    # standup the db's
    user_repo = UserRepository('db/users.json')
    session_repo = SessionRepository('db/sessions.json')
    
    # TODO: wire up scheduling services for sessions and repository
    member_service = MemberService(user_repo)
    session_service = SessionService(session_repo)

    me = member_service.create("TOM")
    session = session_service.create(me, datetime.now(), [me])
    all_sessions = session_service.list_users_sessions(me)
    for sesh in all_sessions:
        print(sesh.id)
    cal = Calendar(me)

    print(cal.list_sessions())

if __name__ == "__main__":
    main()
