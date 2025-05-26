import argparse

from scheduling.member import MemberService
from scheduling.session import SessionService
from scheduling.response import ProposalService, Response

from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository

class Context:
    """
    A class that allows storing and accessing arbitrary objects using attribute-style access.
    """
    def __init__(self):
        """
        Initialize an empty Context.
        """
        ...

    def set(self, name, obj):
        """
        Sets an object on the Context with the given name.

        Args:
            name (str): The name under which the object will be stored.
            obj (object): The object to store (e.g., an instance of a service class).
        """
        setattr(self, name, obj)  

class CLIHelpers:
    """methods only needed when presentation layer is CLI"""
    def get_all_users_helper(self, ctx):
        all_users = ctx.member_service.get_all_users()
        print(all_users)
    
    def handle_invite_response_helper(self, ctx, session_id, user, response, proposal=None):
        if response == "yes":
            ctx.session_service.handle_response(session_id, user, Response.YES)
        elif response == "no":
            ctx.session_service.handle_response(session_id, user, Response.NO)
        elif response == "newtimes":
            if not proposal:
                raise ValueError("If you respond with `newtimes` you must provide a proposal `-p`")
            prop = ctx.proposal_service.make_new_proposal(proposal[0], proposal[1], user)
            ctx.session_service.handle_response(session_id, user, Response.PROPOSAL, proposal=prop)
        else:
            raise ValueError("Invalid response")

def setup() -> Context:
    # standup the db's
    user_repo = UserRepository('db/users.json')
    session_repo = SessionRepository('db/sessions.json')
    
    member_service = MemberService(user_repo)
    proposal_service = ProposalService(member_service)
    session_service = SessionService(session_repo, member_service, proposal_service)   
    
    ctx = Context()
    ctx.set("member_service", member_service)
    ctx.set("session_service", session_service)
    ctx.set("proposal_service", proposal_service) 

    return ctx

def create_parser(ctx, helper_funcs):
    """Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description="CLI tool for GMCal.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for creating a session
    add_parser = subparsers.add_parser("create", help="Create a new scheduling session")
    add_parser.add_argument("creator", help="The user creating the session")
    add_parser.add_argument("start", help="Datetime of the session start in ISO format (YYYY-MM-DDTHH:MM:SS)")
    add_parser.add_argument("end", help="Datetime of the session end in ISO format (YYYY-MM-DDTHH:MM:SS)")
    add_parser.add_argument("-u", "--users", nargs='+', help="List of users to invite (space-separated)")
    add_parser.set_defaults(func=lambda args: ctx.session_service.create(args.creator, args.start, args.end, args.users))

    # Subparser for creating a user
    user_parser = subparsers.add_parser("user", help="create a new user")
    user_parser.add_argument("name", help="name of the user to add")
    user_parser.set_defaults(func=lambda args: ctx.member_service.create(args.name))

    user_list_parser = subparsers.add_parser("list-users", help="list all users currently in system")
    user_list_parser.set_defaults(func=lambda args: helper_funcs.get_all_users_helper(ctx))

    # Subparser for listing responses
    # responses_parser = subparsers.add_parser("responses", help="List responses for a specific session")
    # responses_parser.add_argument("session_id", help="ID of the session to list responses for")
    # responses_parser.set_defaults(func=list_responses)

    # Subparser for responding to a session
    respond_parser = subparsers.add_parser("respond", help="Respond to an invitation for a session")
    respond_parser.add_argument("session_id", help="ID of the session to respond to")
    respond_parser.add_argument("user", help="Your username")
    respond_parser.add_argument("response", choices=['yes', 'no', 'newtimes'], help="Your response to the invitation")
    respond_parser.add_argument("-p", "--proposal", nargs='+', help="two datetimes for start end (space-separated)")
    respond_parser.set_defaults(func=lambda args: helper_funcs.handle_invite_response_helper(ctx, args.session_id, args.user, args.response, args.proposal))
    # respond_parser.set_defaults(func=respond_to_session)

    return parser

def main():
    ctx = setup()
    cli_helpers = CLIHelpers()
    # TODO: optionally set up the parser based on an env var or something. use Sanic otherwise
    parser = create_parser(ctx, cli_helpers)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
