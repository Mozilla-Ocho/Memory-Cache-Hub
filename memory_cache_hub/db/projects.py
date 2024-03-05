from sqlmodel import Field, Session, SQLModel, create_engine
from memory_cache_hub.db.types import Project

def db_create_project(db, project_name: str):
    with Session(db) as session:
        project = Project(name=project_name)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

def db_list_projects(db):
    with Session(db) as session:
        projects = session.query(Project).all()
        return projects

def db_get_project(db, project_id: int):
    with Session(db) as session:
        project = session.query(Project).get(project_id)
        return project

def db_delete_project(db, project_id: int):
    with Session(db) as session:
        project = session.query(Project).get(project_id)
        session.delete(project)
        session.commit()
        return project
