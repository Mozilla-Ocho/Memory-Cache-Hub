from sqlmodel import Field, Session, SQLModel, create_engine
from memory_cache_hub.db.types import Project, ProjectDirectory

def db_create_project(db, project_name: str):
    with Session(db) as session:
        project = Project(name=project_name)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

def db_list_projects(db):
    with Session(db) as session:
        projects = session.query(Project).filter(Project.is_removed == False).all()
        return projects

def db_get_project(db, project_id: int):
    with Session(db) as session:
        project = session.query(Project).get(project_id)
        return project

def db_delete_project(db, project_id: int):
    with Session(db) as session:
        project = session.query(Project).get(project_id)
        project.is_removed = True
        # session.add(project)
        session.commit()
        session.refresh(project)
        return project

def db_create_project_directory(db, project_id: int, path: str):
    with Session(db) as session:
        project = session.query(Project).get(project_id)
        project_directory = ProjectDirectory(path=path, project_id=project.id)
        session.add(project_directory)
        session.commit()
        session.refresh(project_directory)
        return project_directory

def db_list_project_directories(db, project_id: int):
    with Session(db) as session:
        project_directories = session.query(ProjectDirectory).filter(ProjectDirectory.project_id == project_id, ProjectDirectory.is_removed == False).all()
        return project_directories

def db_delete_project_directory(db, directory_id: int):
    print("Deleting project directory: " + str(directory_id))
    with Session(db) as session:
        project_directory = session.query(ProjectDirectory).get(directory_id)
        project_directory.is_removed = True
        # session.add(project_directory)
        session.commit()
        session.refresh(project_directory)
        return project_directory
