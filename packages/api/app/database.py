import os

if os.getenv("USE_PRISMA"):
    from .prisma_db import PrismaDB
    DB = PrismaDB()
else:
    from .db import InMemoryDB
    DB = InMemoryDB()
