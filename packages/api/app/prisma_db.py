"""Implémentation initiale d'une base PostgreSQL via Prisma."""

import asyncio
from typing import List

from prisma import Prisma
from .models import TrainingSession


class PrismaDB:
    """Client Prisma simplifié pour stocker les séances."""

    def __init__(self) -> None:
        self.client = Prisma()
        self._connected = False

    async def connect(self) -> None:
        if not self._connected:
            await self.client.connect()
            self._connected = True

    async def disconnect(self) -> None:
        if self._connected:
            await self.client.disconnect()
            self._connected = False

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    def add_session(self, session: TrainingSession) -> TrainingSession:
        async def _create():
            record = await self.client.session.create(
                data={
                    "date": session.date,
                    "sport": session.sport,
                    "durationMin": session.duration_min,
                    "rpe": session.rpe or 0,
                }
            )
            session.id = record.id
            return session

        return self._run(_create())

    def list_sessions(self) -> List[TrainingSession]:
        async def _list():
            records = await self.client.session.find_many(order={"id": "asc"})
            return [
                TrainingSession(
                    id=r.id,
                    date=r.date,
                    sport=r.sport,
                    duration_min=r.durationMin,
                    rpe=r.rpe,
                )
                for r in records
            ]

        return self._run(_list())

    def get_session(self, session_id: int) -> TrainingSession:
        async def _get():
            r = await self.client.session.find_unique(where={"id": session_id})
            if not r:
                return None
            return TrainingSession(
                id=r.id,
                date=r.date,
                sport=r.sport,
                duration_min=r.durationMin,
                rpe=r.rpe,
            )

        return self._run(_get())

    def update_session(self, session_id: int, session: TrainingSession) -> TrainingSession:
        async def _update():
            await self.client.session.update(
                where={"id": session_id},
                data={
                    "date": session.date,
                    "sport": session.sport,
                    "durationMin": session.duration_min,
                    "rpe": session.rpe or 0,
                },
            )
            return session

        return self._run(_update())

    # Les autres méthodes (nutrition, blessures, etc.) restent à implémenter
