from typing import Dict, List
from .models import TrainingSession, NutritionEntry, Injury, Competition
from datetime import date, timedelta

"""Persistance des données.

Cette implémentation en mémoire sert uniquement de prototype. Pour rendre
l'application opérationnelle (voir point 1 du fichier TODO.md), il faudra la
remplacer par une base de données réelle, par exemple PostgreSQL via Prisma ou
SQLAlchemy. Toutes les méthodes devront alors effectuer les requêtes nécessaires
et gérer les migrations.
"""

class InMemoryDB:
    def __init__(self):
        self._sessions: Dict[int, TrainingSession] = {}
        self._order: List[int] = []
        self._nutrition: Dict[int, NutritionEntry] = {}
        self._injuries: Dict[int, Injury] = {}
        self._competitions: Dict[int, Competition] = {}
        self._counter = 1
        self._nutrition_counter = 1
        self._injury_counter = 1
        self._competition_counter = 1

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

    # Competitions
    def add_competition(self, comp: Competition) -> Competition:
        comp.id = self._competition_counter
        self._competition_counter += 1
        self._competitions[comp.id] = comp
        return comp

    def list_competitions(self) -> List[Competition]:
        return list(self._competitions.values())

DB = InMemoryDB()
