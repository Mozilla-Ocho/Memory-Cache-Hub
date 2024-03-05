from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

def initialize_sqlite_db(sqlite_db_path: str):
    engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine
