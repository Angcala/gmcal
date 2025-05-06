from scheduling.calendar import Calendar
from scheduling.member import Member
from scheduling.session import Session


def main():
    me = Member("TOM")

    cal = Calendar(me)

    print(cal.list_sessions())

if __name__ == "__main__":
    main()
