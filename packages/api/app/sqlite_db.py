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
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS nutrition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                calories INTEGER,
                hydration_l REAL,
                carbs_g INTEGER,
                protein_g INTEGER,
                fat_g INTEGER
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS injuries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date TEXT NOT NULL,
                end_date TEXT,
                description TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                name TEXT
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

    def add_nutrition(self, entry: NutritionEntry) -> NutritionEntry:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO nutrition (date, calories, hydration_l, carbs_g, protein_g, fat_g)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                entry.date.isoformat(),
                entry.calories,
                entry.hydration_l,
                entry.carbs_g,
                entry.protein_g,
                entry.fat_g,
            ),
        )
        self.conn.commit()
        entry.id = cur.lastrowid
        return entry

    def list_nutrition(self) -> List[NutritionEntry]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM nutrition ORDER BY id ASC")
        rows = cur.fetchall()
        return [
            NutritionEntry(
                id=row["id"],
                date=date.fromisoformat(row["date"]),
                calories=row["calories"],
                hydration_l=row["hydration_l"],
                carbs_g=row["carbs_g"],
                protein_g=row["protein_g"],
                fat_g=row["fat_g"],
            )
            for row in rows
        ]

    def add_injury(self, injury: Injury) -> Injury:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO injuries (start_date, end_date, description) VALUES (?, ?, ?)",
            (
                injury.start_date.isoformat(),
                injury.end_date.isoformat() if injury.end_date else None,
                injury.description,
            ),
        )
        self.conn.commit()
        injury.id = cur.lastrowid
        return injury

    def list_injuries(self) -> List[Injury]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM injuries ORDER BY id ASC")
        rows = cur.fetchall()
        return [
            Injury(
                id=row["id"],
                start_date=date.fromisoformat(row["start_date"]),
                end_date=date.fromisoformat(row["end_date"]) if row["end_date"] else None,
                description=row["description"] or "",
            )
            for row in rows
        ]

    def add_competition(self, comp: Competition) -> Competition:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO competitions (date, name) VALUES (?, ?)",
            (
                comp.date.isoformat(),
                comp.name,
            ),
        )
        self.conn.commit()
        comp.id = cur.lastrowid
        return comp

    def list_competitions(self) -> List[Competition]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM competitions ORDER BY id ASC")
        rows = cur.fetchall()
        return [
            Competition(
                id=row["id"],
                date=date.fromisoformat(row["date"]),
                name=row["name"] or "",
            )
            for row in rows
        ]
