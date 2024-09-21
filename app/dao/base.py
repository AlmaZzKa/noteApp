from sqlalchemy.future import select
from app.database import async_session_maker


class BaseDAO:
    model = None

