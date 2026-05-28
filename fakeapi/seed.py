import copy

from fakeapi.projects.provider import projects_seed
from fakeapi.tasks.provider import tasks_seed
from fakeapi.users.provider import users_seed


def get_seed_snapshot() -> dict[str, list[dict]]:
    return {
        "tasks": copy.deepcopy(tasks_seed),
        "users": copy.deepcopy(users_seed),
        "projects": copy.deepcopy(projects_seed),
    }
