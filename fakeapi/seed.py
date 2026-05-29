import copy

from fakeapi.api.projects.provider import projects_seed
from fakeapi.api.tasks.provider import tasks_seed
from fakeapi.api.users.provider import users_seed


def get_seed_snapshot() -> dict[str, list[dict]]:
    return {
        "tasks": copy.deepcopy(tasks_seed),
        "users": copy.deepcopy(users_seed),
        "projects": copy.deepcopy(projects_seed),
    }
