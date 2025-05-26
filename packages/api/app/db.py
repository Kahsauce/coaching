from typing import Dict, List
from .models import TrainingSession, NutritionEntry, Injury, Competition
from datetime import date, timedelta

"""Persistance des données.

L'implémentation d'origine utilisait une base en mémoire pour faciliter le
prototypage. Le point 1 du fichier TODO.md demande de passer à une base
persistante. Ce module propose d'utiliser par défaut SQLite mais permet de
sélectionner d'autres backends via la variable d'environnement ``COACHING_DB``.
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

    def update_injury(self, injury_id: int, injury: Injury) -> Injury:
        self._injuries[injury_id] = injury
        injury.id = injury_id
        return injury

    # Competitions
    def add_competition(self, comp: Competition) -> Competition:
        comp.id = self._competition_counter
        self._competition_counter += 1
        self._competitions[comp.id] = comp
        return comp

    def list_competitions(self) -> List[Competition]:
        return list(self._competitions.values())

import os
from .sqlite_db import SQLiteDB

PrismaDB = None
if os.getenv("COACHING_DB") == "prisma":
    try:
        from .prisma_db import PrismaDB as _PrismaDB
        PrismaDB = _PrismaDB
    except Exception:  # pragma: no cover - optional dependency
        PrismaDB = None

backend = os.getenv("COACHING_DB", "sqlite")

if backend == "prisma":
    if PrismaDB is None:
        raise ImportError("Prisma backend requested but prisma module not available")
    DB = PrismaDB()
elif backend == "memory":
    DB = InMemoryDB()
else:
    path = os.getenv("COACHING_DB_PATH", "coaching.db")
    DB = SQLiteDB(path)
