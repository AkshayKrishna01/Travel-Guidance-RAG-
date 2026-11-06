# repositories/knowledge_base_repository.py
import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.models import Base, KnowledgeBase  
from ..database.database_connection import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeBaseRepository:
    def __init__(self):
        self.db = Database()

    def _get_session(self) -> Session:
        try:
            return self.db.SessionLocal()
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            raise Exception("DB_CONNECTION_ERROR")

    def create_knowledgebase_repo(
        self,
        chunks: List[str],
        vector_points: List[List[float]],
        created_by: Optional[str] = "admin",
        updated_by: Optional[str] = "admin",
        is_active: bool = True,
    ) -> List[KnowledgeBase]:
        session: Optional[Session] = None

        try:
            Base.metadata.create_all(self.db.engine)
            print("All ORM tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)

        try:
            session = self._get_session()
            now = datetime.utcnow()
            rows: List[KnowledgeBase] = []

            for chunk, vec in zip(chunks, vector_points):
                row = KnowledgeBase(
                    description=str(chunk),
                    vector_points=vec,
                    created_at=now,
                    updated_at=now,
                    created_by=created_by,
                    updated_by=updated_by,
                    is_active=is_active,
                )
                session.add(row)
                rows.append(row)

            session.commit()
            print("Stored Successfully")
            return rows

        except SQLAlchemyError as e:
            if session:
                session.rollback()
            logger.exception("Error while inserting knowledge base rows")
            raise Exception("KNOWLEDGE_BASE_CREATE_FAILED") from e
        finally:
            if session:
                session.close()

    def similarity_search(self, embeddings: List[float], top_k: int = 4) -> str:
        session = None
        try:
            session = self._get_session()

            distance_expr = KnowledgeBase.vector_points.cosine_distance(embeddings)

            stmt = (
                select(KnowledgeBase.description)
                .where(KnowledgeBase.is_active.is_(True))  
                .order_by(distance_expr.asc())
                .limit(top_k)
            )

            rows = session.execute(stmt).all()
            descriptions = [row[0] for row in rows]

            return "\n\n---\n\n".join(descriptions)
        except Exception as e:
            logger.error(f"Similarity search error: {e}")
            Exception("SIMILARITY_SEARCH_FAILED")
        finally:
            if session:
                session.close()

    # def similarity_search(self, embeddings: List[float]) -> str:

    #     session: Optional[Session] = None
    #     try:
    #         session = self._get_session()

    #         smt = session.execute(text("""
    #         SELECT description
    #         FROM Akshay_embedding_data
    #         ORDER BY vector_points <-> :vec
    #          LIMIT 2"""), {"vec":str(embeddings)})
    #         result =""
 
    #         for row in smt:
    #             result = f"{result}" + f"{str(row.description)}"
    #         return result

    #     except Exception as e:
    #         logger.error(f"Similarity search error: {e}")
    #         raise Exception("SIMILARITY_SEARCH_FAILED")
    #     finally:
    #         if session:
    #             session.close()
