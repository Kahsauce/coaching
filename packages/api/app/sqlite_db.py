import sqlite3
from datetime import date
from typing import List

from .models import TrainingSession, NutritionEntry, Injury, Competition

class SQLiteDB:
    """Stockage persistant minimal utilisant SQLite."""

    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER,
                date TEXT NOT NULL,
                sport TEXT NOT NULL,
                description TEXT,
                duration_min INTEGER,
                rpe INTEGER,
                completed INTEGER
            )
            """
        )
        self.conn.commit()

    def _next_position(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COALESCE(MAX(position), 0) + 1 FROM sessions")
        return cur.fetchone()[0]

    def add_session(self, session: TrainingSession) -> TrainingSession:
        cur = self.conn.cursor()
        pos = self._next_position()
        cur.execute(
            "INSERT INTO sessions (position, date, sport, description, duration_min, rpe, completed) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                pos,
                session.date.isoformat(),
                session.sport,
                session.description,
                session.duration_min,
                session.rpe,
                int(session.completed),
            ),
        )
        self.conn.commit()
        session.id = cur.lastrowid
        return session

    def list_sessions(self) -> List[TrainingSession]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM sessions ORDER BY position ASC"
        )
        rows = cur.fetchall()
        return [
            TrainingSession(
                id=row["id"],
                date=date.fromisoformat(row["date"]),
                sport=row["sport"],
                description=row["description"] or "",
                duration_min=row["duration_min"],
                rpe=row["rpe"],
                completed=bool(row["completed"]),
            )
            for row in rows
        ]

    def get_session(self, session_id: int) -> TrainingSession:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sessions WHERE id=?", (session_id,))
        row = cur.fetchone()
        if not row:
            return None
        return TrainingSession(
            id=row["id"],
            date=date.fromisoformat(row["date"]),
            sport=row["sport"],
            description=row["description"] or "",
            duration_min=row["duration_min"],
            rpe=row["rpe"],
            completed=bool(row["completed"]),
        )

    def update_session(self, session_id: int, session: TrainingSession) -> TrainingSession:
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE sessions
            SET date=?, sport=?, description=?, duration_min=?, rpe=?, completed=?
            WHERE id=?
            """,
            (
                session.date.isoformat(),
                session.sport,
                session.description,
                session.duration_min,
                session.rpe,
                int(session.completed),
                session_id,
            ),
        )
        self.conn.commit()
        return session

    def reorder_sessions(self, new_order: List[int]) -> List[TrainingSession]:
        cur = self.conn.cursor()
        for pos, sid in enumerate(new_order, start=1):
            cur.execute("UPDATE sessions SET position=? WHERE id=?", (pos, sid))
        self.conn.commit()
        return self.list_sessions()

    # For now, other data remain in memory
    def add_nutrition(self, entry: NutritionEntry) -> NutritionEntry:
        raise NotImplementedError

    def list_nutrition(self) -> List[NutritionEntry]:
        return []

    def add_injury(self, injury: Injury) -> Injury:
        raise NotImplementedError

    def list_injuries(self) -> List[Injury]:
        return []

    def add_competition(self, comp: Competition) -> Competition:
        raise NotImplementedError

    def list_competitions(self) -> List[Competition]:
        return []
