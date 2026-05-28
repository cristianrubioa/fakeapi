from datetime import UTC
from datetime import datetime
from datetime import timedelta

users_seed: list[dict] = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "role": "admin",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC),
    },
    {
        "id": 2,
        "name": "Bob Martinez",
        "email": "bob.martinez@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=10),
    },
    {
        "id": 3,
        "name": "Carol White",
        "email": "carol.white@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=20),
    },
    {
        "id": 4,
        "name": "David Kim",
        "email": "david.kim@example.com",
        "role": "viewer",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=30),
    },
    {
        "id": 5,
        "name": "Eva Chen",
        "email": "eva.chen@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=40),
    },
    {
        "id": 6,
        "name": "Frank Torres",
        "email": "frank.torres@example.com",
        "role": "admin",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=50),
    },
    {
        "id": 7,
        "name": "Grace Lee",
        "email": "grace.lee@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=60),
    },
    {
        "id": 8,
        "name": "Henry Patel",
        "email": "henry.patel@example.com",
        "role": "viewer",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=70),
    },
    {
        "id": 9,
        "name": "Isabella Nguyen",
        "email": "isabella.nguyen@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=80),
    },
    {
        "id": 10,
        "name": "James Brown",
        "email": "james.brown@example.com",
        "role": "member",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=90),
    },
]
