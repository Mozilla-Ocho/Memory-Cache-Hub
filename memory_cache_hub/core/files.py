import os
import shutil

def get_project_uploads_directory(root_directory: str, project_name: str):
    return os.path.join(root_directory, "uploads", project_name)

def get_project_summaries_directory(root_directory: str, project_name: str):
    return os.path.join(root_directory, "summaries", project_name)

def get_file_summary_path(root_directory: str, project_name: str, file_path: str):
    return os.path.join(get_project_summaries_directory(root_directory, project_name), file_path + ".summary.md")

def _write_file(full_path: str, content: str):
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as file:
        file.write(content)

# TODO save -> write
def write_file_upload(root_directory: str, project_name: str, file_path: str, file):
    try:
        project_uploads_directory = get_project_uploads_directory(root_directory, project_name)
        target_path = os.path.join(project_uploads_directory, file_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()


def write_file_summary(root_directory: str, project_name: str, file_path: str, summary: str):
    project_summaries_directory = get_project_summaries_directory(root_directory, project_name)
    target_path = os.path.join(project_summaries_directory, file_path + ".summary.md")
    _write_file(target_path, summary)

# TODO Rename create -> make AND directory -> directories
def create_empty_project_directory(root_directory:str, project_name: str):
    project_uploads_directory = get_project_uploads_directory(root_directory, project_name)
    project_summaries_directory = get_project_summaries_directory(root_directory, project_name)
    os.makedirs(project_uploads_directory, exist_ok=True)
    os.makedirs(project_summaries_directory, exist_ok=True)

# TODO Rename delete_file -> delete_uploaded_file
def delete_file(root_directory: str, project_name: str, file_path: str):
    project_uploads_directory = get_project_uploads_directory(root_directory, project_name)
    target_path = os.path.join(project_uploads_directory, file_path)
    if os.path.exists(target_path):
        os.remove(target_path)
        return True
    else:
        return False

# TODO Rename directory -> directories
def delete_project_directory(root_directory: str, project_name: str):
    project_uploads_directory = get_project_uploads_directory(root_directory, project_name)
    project_summaries_directory = get_project_summaries_directory(root_directory, project_name)
    if os.path.exists(project_uploads_directory):
        shutil.rmtree(project_uploads_directory)
    if os.path.exists(project_summaries_directory):
        shutil.rmtree(project_summaries_directory)
    return True

def get_file_summary(root_directory: str, project_name: str, file_path: str):
    file_summary_path = get_file_summary_path(root_directory, project_name, file_path)
    with open(file_summary_path, "r") as file:
        return file.read()

def list_project_file_uploads(root_directory: str, project_name: str):
    project_uploads_directory = get_project_uploads_directory(root_directory, project_name)
    files_list = []
    for root, _, files in os.walk(project_uploads_directory):
        for file in files:
            # Calculate the relative path from root_directory to the file
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_directory)
            files_list.append(relative_path)
    return files_list

def list_project_file_summaries(root_directory: str, project_name: str):
    project_summaries_directory = get_project_summaries_directory(root_directory, project_name)
    files_list = []
    for root, _, files in os.walk(project_summaries_directory):
        for file in files:
            # Calculate the relative path from root_directory to the file
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_directory)
            files_list.append(relative_path)
    return files_list
