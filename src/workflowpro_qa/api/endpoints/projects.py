PROJECTS = "/api/v1/projects"


def project_by_id(project_id: int | str) -> str:
    return f"{PROJECTS}/{project_id}"
