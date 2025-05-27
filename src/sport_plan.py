import json
import os
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from typing import List, Dict

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

@dataclass
class UserProfile:
    name: str
    age: int
    weight: float
    height: float
    sports: List[str]

@dataclass
class Session:
    date: str  # ISO format
    activity_type: str
    duration: int  # minutes
    rpe: int  # 1-10

    @property
    def srpe(self) -> int:
        return self.duration * self.rpe

def load_data() -> Dict:
    if not os.path.exists(DATA_FILE):
        return {"profiles": [], "sessions": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data: Dict) -> None:
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def add_profile(profile: UserProfile) -> None:
    data = load_data()
    data.setdefault("profiles", []).append(asdict(profile))
    save_data(data)

def add_session(session: Session) -> None:
    data = load_data()
    data.setdefault("sessions", []).append(asdict(session))
    save_data(data)

def list_sessions() -> List[Session]:
    data = load_data()
    return [Session(**s) for s in data.get("sessions", [])]

def compute_acute_load(sessions: List[Session], today: date) -> int:
    start = today - timedelta(days=6)
    return sum(s.srpe for s in sessions if start <= datetime.fromisoformat(s.date).date() <= today)

def compute_chronic_load(sessions: List[Session], today: date) -> float:
    start = today - timedelta(days=27)
    loads = [s.srpe for s in sessions if start <= datetime.fromisoformat(s.date).date() <= today]
    if not loads:
        return 0.0
    return sum(loads) / 4  # average weekly over 4 weeks

def compute_acwr(sessions: List[Session], today: date) -> float:
    chronic = compute_chronic_load(sessions, today)
    if chronic == 0:
        return 0.0
    acute = compute_acute_load(sessions, today)
    return acute / chronic

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Gestion sportive simplifiée")
    subparsers = parser.add_subparsers(dest="command")

    add_prof_parser = subparsers.add_parser("add-profile")
    add_prof_parser.add_argument("name")
    add_prof_parser.add_argument("age", type=int)
    add_prof_parser.add_argument("weight", type=float)
    add_prof_parser.add_argument("height", type=float)
    add_prof_parser.add_argument("sports", nargs='+')

    add_sess_parser = subparsers.add_parser("add-session")
    add_sess_parser.add_argument("date")
    add_sess_parser.add_argument("activity_type")
    add_sess_parser.add_argument("duration", type=int)
    add_sess_parser.add_argument("rpe", type=int)

    metrics_parser = subparsers.add_parser("metrics")
    metrics_parser.add_argument("date")

    args = parser.parse_args()

    if args.command == "add-profile":
        profile = UserProfile(args.name, args.age, args.weight, args.height, args.sports)
        add_profile(profile)
        print("Profil ajouté.")
    elif args.command == "add-session":
        session = Session(args.date, args.activity_type, args.duration, args.rpe)
        add_session(session)
        print("Séance ajoutée.")
    elif args.command == "metrics":
        today = datetime.fromisoformat(args.date).date()
        sessions = list_sessions()
        acute = compute_acute_load(sessions, today)
        chronic = compute_chronic_load(sessions, today)
        acwr = compute_acwr(sessions, today)
        print(f"Charge aiguë: {acute}")
        print(f"Charge chronique: {chronic}")
        print(f"ACWR: {acwr:.2f}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
