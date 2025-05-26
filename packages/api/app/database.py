import os

if os.getenv("USE_PRISMA"):
    from .prisma_db import PrismaDB
    DB = PrismaDB()
elif os.getenv("USE_SQLITE"):
    from .sqlite_db import SQLiteDB
    DB = SQLiteDB()
else:
    from .db import InMemoryDB
    DB = InMemoryDB()
