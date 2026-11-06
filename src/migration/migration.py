from sqlalchemy import inspect

from ..models.models import KnowledgeBase
from ..database.database_connection import Database


TABLE_ORDER_CREATION = [
    KnowledgeBase.__tablename__,
]

MODEL_CLASSES = {
    KnowledgeBase.__tablename__:"Akshay_KnowledgeBase",
}


class Migration:
    def __init__(self):
        self.db = Database()
        self.engine = self.db.engine
        self.inspector = inspect(self.engine)

    def create_tables(self):
        for table_name in TABLE_ORDER_CREATION:
            if not self.inspector.has_table(table_name):
                MODEL_CLASSES[table_name].__table__.create(bind=self.engine)
