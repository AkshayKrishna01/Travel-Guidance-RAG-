from sqlalchemy.orm import Session
from ..database.database_connection import Database
from ..models.models import KnowledgeBase

class Seeder:
    def __init__(self):
        self.db = Database()
    
   