from typing import Dict
from .models import TrainingSession

class InMemoryDB:
    def __init__(self):
        self._sessions: Dict[int, TrainingSession] = {}
        self._counter = 1

    def add_session(self, session: TrainingSession) -> TrainingSession:
        session.id = self._counter
        self._counter += 1
        self._sessions[session.id] = session
        return session

    def list_sessions(self):
        return list(self._sessions.values())

    def get_session(self, session_id: int) -> TrainingSession:
        return self._sessions.get(session_id)

    def update_session(self, session_id: int, session: TrainingSession) -> TrainingSession:
        self._sessions[session_id] = session
        return session

DB = InMemoryDB()
