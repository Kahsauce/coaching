from typing import Dict, List
from .models import TrainingSession, NutritionEntry, Injury
from datetime import date, timedelta

class InMemoryDB:
    def __init__(self):
        self._sessions: Dict[int, TrainingSession] = {}
        self._order: List[int] = []
        self._nutrition: Dict[int, NutritionEntry] = {}
        self._injuries: Dict[int, Injury] = {}
        self._counter = 1
        self._nutrition_counter = 1
        self._injury_counter = 1

    def add_session(self, session: TrainingSession) -> TrainingSession:
        session.id = self._counter
        self._counter += 1
        self._sessions[session.id] = session
        self._order.append(session.id)
        return session

    def list_sessions(self):
        return [self._sessions[sid] for sid in self._order]

    def get_session(self, session_id: int) -> TrainingSession:
        return self._sessions.get(session_id)

    def update_session(self, session_id: int, session: TrainingSession) -> TrainingSession:
        self._sessions[session_id] = session
        return session

    def reorder_sessions(self, new_order: List[int]) -> List[TrainingSession]:
        self._order = [sid for sid in new_order if sid in self._sessions]
        return self.list_sessions()

    def sessions_for_week(self, start: date) -> List[TrainingSession]:
        end = start + timedelta(days=6)
        return [s for s in self.list_sessions() if start <= s.date <= end]

    # Nutrition entries
    def add_nutrition(self, entry: NutritionEntry) -> NutritionEntry:
        entry.id = self._nutrition_counter
        self._nutrition_counter += 1
        self._nutrition[entry.id] = entry
        return entry

    def list_nutrition(self) -> List[NutritionEntry]:
        return list(self._nutrition.values())

    # Injuries
    def add_injury(self, injury: Injury) -> Injury:
        injury.id = self._injury_counter
        self._injury_counter += 1
        self._injuries[injury.id] = injury
        return injury

    def list_injuries(self) -> List[Injury]:
        return list(self._injuries.values())

DB = InMemoryDB()
